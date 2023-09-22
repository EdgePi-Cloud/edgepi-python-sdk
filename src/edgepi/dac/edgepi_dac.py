"""
Module for interacting with the EdgePi DAC via SPI.
"""


import logging
from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_constants import (
    NULL_BITS,
    NUM_PINS,
    SW_RESET,
    UPPER_LIMIT,
    PowerMode,
    DACChannel,
    EdgePiDacCom as COM,
    EdgePiDacCalibrationConstants as CalibConst,
    AOPins,
    DOPins,
    GainPin
)
from edgepi.peripherals.spi import SpiDevice as spi
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM

class EdgePiDAC(spi):
    """A EdgePi DAC device"""

    # analog_out number to pin name
    __analog_out_pin_map = {
        DACChannel.AOUT1.value: AOPins.AO_EN1,
        DACChannel.AOUT2.value: AOPins.AO_EN2,
        DACChannel.AOUT3.value: AOPins.AO_EN3,
        DACChannel.AOUT4.value: AOPins.AO_EN4,
        DACChannel.AOUT5.value: AOPins.AO_EN5,
        DACChannel.AOUT6.value: AOPins.AO_EN6,
        DACChannel.AOUT7.value: AOPins.AO_EN7,
        DACChannel.AOUT8.value: AOPins.AO_EN8,
    }

    # analog_out number to DOUT pin pair
    __analog_to_digital_pin_map = {
        DACChannel.AOUT1.value: DOPins.DOUT1,
        DACChannel.AOUT2.value: DOPins.DOUT2,
        DACChannel.AOUT3.value: DOPins.DOUT3,
        DACChannel.AOUT4.value: DOPins.DOUT4,
        DACChannel.AOUT5.value: DOPins.DOUT5,
        DACChannel.AOUT6.value: DOPins.DOUT6,
        DACChannel.AOUT7.value: DOPins.DOUT7,
        DACChannel.AOUT8.value: DOPins.DOUT8,
    }



    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing DAC Bus")
        super().__init__(bus_num=6, dev_id=3, mode=1, max_speed=1000000)

        # Read edgepi reserved data and generate calibration parameter dictionary
        eeprom = EdgePiEEPROM()
        eeprom_data  = eeprom.read_edgepi_data()
        dac_calib_params = eeprom_data.dac_calib_params.extract_ch_dict()

        self.dac_ops = DACCommands(dac_calib_params)
        self.gpio = EdgePiGPIO()

        self.__dac_power_state = {
            DACChannel.AOUT8.value: PowerMode.NORMAL.value,
            DACChannel.AOUT7.value: PowerMode.NORMAL.value,
            DACChannel.AOUT6.value: PowerMode.NORMAL.value,
            DACChannel.AOUT5.value: PowerMode.NORMAL.value,
            DACChannel.AOUT4.value: PowerMode.NORMAL.value,
            DACChannel.AOUT3.value: PowerMode.NORMAL.value,
            DACChannel.AOUT2.value: PowerMode.NORMAL.value,
            DACChannel.AOUT1.value: PowerMode.NORMAL.value,
        }

    def __send_to_gpio_pins(self, analog_out: int, voltage: float):
        ao_pin = self.__analog_out_pin_map[analog_out].value
        do_pin = self.__analog_to_digital_pin_map[analog_out].value
        if voltage > 0:
            if analog_out in [DACChannel.AOUT1.value, DACChannel.AOUT2.value]:
                self.__dac_switching_logic(analog_out)
            self.gpio.set_pin_state(ao_pin)
            self.gpio.clear_pin_state(do_pin)
        elif voltage == 0:
            if analog_out in [DACChannel.AOUT2.value,DACChannel.AOUT1.value]:
                self.__dac_switching_logic(analog_out)
            self.gpio.set_pin_state(ao_pin)
            self.gpio.clear_pin_state(do_pin)
            self.gpio.clear_pin_state(ao_pin)
        else:
            raise ValueError("voltage cannot be negative")

    def __dac_switching_logic(self, analog_out: int):
        """
        In order to attach DAC output to the terminal block, proper swtiching of GPIO should happen.
        AOUT1 and AOUT2 have special switching logic.

        Args:
            `analog_out` (DACChannel): A/D_OUT pin to write a voltage value to.
        """
        pwm_en = GpioPins.PWM1 if analog_out == DACChannel.AOUT1.value else GpioPins.PWM2
        self.gpio.set_pin_direction_out(pwm_en.value)
        self.gpio.set_pin_state(pwm_en.value)

    # TODO: Decimal instead of float for precision testing
    def write_voltage(self, analog_out: DACChannel, voltage: float):
        """
        Write a voltage value to an analog out pin. Voltage will be continuously
        transmitted to the analog out pin until a 0 V value is written to it.

        Args:
            `analog_out` (DACChannel): A/D_OUT pin to write a voltage value to.

            `voltage` (float): the voltage value to write, in volts.

        Raises:
            `ValueError`: if voltage has more decimal places than DAC accuracy limit
        """
        dac_gain = CalibConst.DAC_GAIN_FACTOR.value if self.__get_gain_state() else 1
        self.dac_ops.check_range(analog_out.value, 0, NUM_PINS-1)
        self.dac_ops.check_range(voltage, 0, (UPPER_LIMIT*dac_gain))
        code = self.dac_ops.voltage_to_code(analog_out.value, voltage, dac_gain)
        self.log.debug(f'Code: {code}')

        # update DAC register
        with self.spi_open():
            self.transfer(self.dac_ops.generate_write_and_update_command(analog_out.value, code))
        # send voltage to analog out pin
        self.__send_to_gpio_pins(analog_out.value, voltage)
        return code

    def set_power_mode(self, analog_out: DACChannel, power_mode: PowerMode):
        """
        Set power mode for individual DAC channels to either normal power consumption,
        or low power consumption modes.

        For example, this may be of use when no constant power source available.

        Args:
            `analog_out` (DACChannel): the analog out pin whose power mode will be changed

            `power_mode` (PowerMode): a valid hex code for setting DAC channel power mode
        """
        self.dac_ops.check_range(analog_out.value, 0, NUM_PINS-1)
        self.__dac_power_state[analog_out.value] = power_mode.value
        power_code = self.dac_ops.generate_power_code(self.__dac_power_state.values())
        cmd = self.dac_ops.combine_command(COM.COM_POWER_DOWN_OP.value, NULL_BITS, power_code)
        with self.spi_open():
            self.transfer(cmd)

    def reset(self):
        """
        Performs a software reset of the EdgePi DAC to power-on default values,
        and stops all voltage transmissions through pins.
        """
        cmd = self.dac_ops.combine_command(COM.COM_SW_RESET.value, NULL_BITS, SW_RESET)
        with self.spi_open():
            self.transfer(cmd)

    def channel_readback(self, analog_out: DACChannel) -> int:
        """
        Readback the input register of DAC.

        Args:
            `analog_out` (DACChannel): the analog out pin to read voltage from
        Return:
            (int): code value stored in the input register, can be used to calculate expected
            voltage
        """
        self.dac_ops.check_range(analog_out.value, 0, NUM_PINS-1)
        # first transfer triggers read mode, second is needed to fetch data
        cmd = self.dac_ops.combine_command(
                COM.COM_READBACK.value, DACChannel(analog_out.value).value, NULL_BITS
            )
        with self.spi_open():
            self.transfer(cmd)
            # all zero dummy command to trigger second transfer which
            # contains the DAC register contents.
            read_data = self.transfer([NULL_BITS, NULL_BITS, NULL_BITS])
        self.log.debug(f"reading code {read_data}")
        return self.dac_ops.extract_read_data(read_data)


    def compute_expected_voltage(self, analog_out: DACChannel) -> float:
        """
        Computes expected voltage from the DAC channel corresponding to analog out pin.
        This is not guaranteed to be the voltage of the analog_out pin at the terminal block,
        nor the voltage being output by the DAC channel. It is a calculation that maps
        the contents of the DAC channel to a voltage value.

        Args:
            analog_out (DACChannel): the analog out pin to read voltage from

        Returns:
            float: the computed voltage value of the DAC channel corresponding
                to the selected analog out pin.
        """
        code = self.channel_readback(analog_out)
        dac_gain = CalibConst.DAC_GAIN_FACTOR.value if self.__get_gain_state() else 1
        return self.dac_ops.code_to_voltage(analog_out.value, code, dac_gain)

    def __compute_code_val(self, set_gain: bool, code: int = None):
        """
        Modify code value depending on the enable flag
        Args:
            set_gain(bool): False: multiply the current code value by 2 if current code value is
                               less than the half of maixmum code value.
                               True: divide the current code value by 2
            code (int): intial code value
        Return:
            code (int): modified code value
        """
        if set_gain:
            return int(code/CalibConst.DAC_GAIN_FACTOR.value)

        code = code*CalibConst.DAC_GAIN_FACTOR.value
        if code > CalibConst.RANGE.value:
            raise ValueError(f"Code Value: {code} is out of range")

        return code

    def __get_ch_codes(self, set_gain: bool):
        """
        Read and modify channel code value
        Args:
            set_gain (bool): False: multiply the current code value by 2
                          True: divide the current code value by 2
        Return:
            code_vals (list): list of code values from ch1-ch8
        """
        code_vals = []
        for ch in DACChannel:
            code, _, _ = self.get_state(ch, True, False, False)
            code_vals.append(self.__compute_code_val(set_gain, code))
        return code_vals

    def __auto_code_handler(self, set_gain: bool):
        """
        Compute and change code values of each channel when toggling DAC gain
        Args:
            set_gain (bool): enable boolean to set or clear the gpio pin
        Return:
            N/A
        """
        codes = self.__get_ch_codes(set_gain)
        self.log.debug(f'Code: {codes}')

        # When the DAC_GAIN is enabled/disabled, the output voltage is doubled/halved instantly.
        # This may damage the circuit that the output is connected to. Therefore, enabling/disabling
        # gain have different steps of sending code value and toggling the GPIO pin.

        # gain being enabled, change code first than enable gain
        with self.spi_open():
            if set_gain:
                for ch, code in enumerate(codes):
                    # update DAC register
                    self.transfer(self.dac_ops.generate_write_and_update_command(ch, code))
                self.gpio.set_pin_state(GainPin.DAC_GAIN.value)

            # Disabling gain, change gain first than change codes
            else:
                self.gpio.clear_pin_state(GainPin.DAC_GAIN.value)
                for ch, code in enumerate(codes):
                    # update DAC register
                    self.transfer(self.dac_ops.generate_write_and_update_command(ch, code))

    def set_dac_gain(self, set_gain: bool, auto_code_change: bool = False):
        """
        Enable/Disable internal DAC gain.
        Args:
            set_gain (bool): True enable DAC gain, False disable DAC gain
            auto_code_change (bool): flag to re-write code value of each channel to keep the same
                                    output voltage
        Return:
            gain_state (bool): state of the gain pin
        """
        # pylint: disable=expression-not-assigned
        # if current gain state is the same as toggle_gain flag, do nothing
        if self.__get_gain_state() == set_gain:
            return set_gain

        if auto_code_change:
            self.__auto_code_handler(set_gain)
        else:
            self.gpio.set_pin_state(GainPin.DAC_GAIN.value) if set_gain else \
            self.gpio.clear_pin_state(GainPin.DAC_GAIN.value)
        return self.__get_gain_state()

    def __get_gain_state(self):
        """
        Retrieve the internal gain state by reading the expander pin
        Args:
            N/A
        Return:
            gain_state (bool): True - gain enalbed, False - gain disabled
        """

        pin_state = self.gpio.read_pin_state(GainPin.DAC_GAIN.value)
        pin_dir = self.gpio.get_pin_direction(GainPin.DAC_GAIN.value)
        if pin_state and not pin_dir:
            return True
        return False

    def get_state(self, analog_out: DACChannel = None,
                        code: bool = None,
                        voltage: bool = None,
                        gain: bool = None):
        """
        the method returns the state of requested parameters. It will either read the register of
        DAC or GPIO expander to retrieve the current state.

        Args:
            analog_out (DACChannel): channel number of interest
            code (bool): requesting the current code value written in the specified channel input
                         register
            voltage (bool): requesting the current expected voltage at the terminal block pin
            gian (bool): requesting the current gain value set for the DAC
        Returns:
            code_val (int): code value read from the input register, None when not requested
            voltage_val (float): voltage calculated using the code value, None when not requested
            gain_state (bool): true if dac gain is enabled or False disabled, None when not
                               requested
        """
        code_val = self.channel_readback(analog_out) if code else None
        voltage_val = self.compute_expected_voltage(analog_out) if voltage else None
        gain_state = self.__get_gain_state() if gain else None
        self.log.debug(f":get_state: state of {analog_out} code {code_val},"
                       f"expected {voltage_val}, dac_gain {gain_state}")
        return code_val, voltage_val, gain_state
