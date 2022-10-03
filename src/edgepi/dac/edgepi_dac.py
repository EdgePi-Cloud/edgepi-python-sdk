"""
Module for interacting with the EdgePi DAC via SPI.
"""


import logging
from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_calibration import (
    DACcalibParam,
    generate_dict_calibration
    )
from edgepi.dac.dac_constants import (
    NULL_BITS,
    NUM_PINS,
    SW_RESET,
    UPPER_LIMIT,
    PowerMode,
    EdgePiDacChannel as CH,
    EdgePiDacCom as COM,
    AOPins,
)
from edgepi.peripherals.spi import SpiDevice as spi
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.gpio_configs import GpioConfigs


_logger = logging.getLogger(__name__)


class EdgePiDAC(spi):
    """A EdgePi DAC device"""

    # analog_out number to pin name
    __analog_out_pin_map = {
        1: AOPins.AO_EN1,
        2: AOPins.AO_EN2,
        3: AOPins.AO_EN3,
        4: AOPins.AO_EN4,
        5: AOPins.AO_EN5,
        6: AOPins.AO_EN6,
        7: AOPins.AO_EN7,
        8: AOPins.AO_EN8,
    }

    # analog_out pins numbered 1-8, DAC channels 0-7
    __analog_out_to_dac_ch = {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 7,
    }

    # TODO: the calib parameter should be saved in an eeprom, and parameters should be read from the
            # eeprom during the class isntantiation instead of this hardcoded value
    __analog_out_calib_param = [[2.5, 0, 5.0, 0], [2.5, 0, 5.0, 0],
                                [2.5, 0, 5.0, 0], [2.5, 0, 5.0, 0],
                                [2.5, 0, 5.0, 0], [2.5, 0, 5.0, 0],
                                [2.5, 0, 5.0, 0], [2.5, 0, 5.0, 0]]

    def __init__(self):
        _logger.info("Initializing DAC Bus")
        super().__init__(bus_num=6, dev_id=3, mode=1, max_speed=1000000)

        self.dac_ops = DACCommands(generate_dict_calibration(DACcalibParam,
                                                             list(
                                                             self.__analog_out_to_dac_ch.values()
                                                             ),
                                                             self.__analog_out_calib_param))
        self.gpio = EdgePiGPIO(GpioConfigs.DAC.value)
        self.gpio.set_expander_default()

        self.__dac_power_state = {
            CH.DAC7.value: PowerMode.NORMAL.value,
            CH.DAC6.value: PowerMode.NORMAL.value,
            CH.DAC5.value: PowerMode.NORMAL.value,
            CH.DAC4.value: PowerMode.NORMAL.value,
            CH.DAC3.value: PowerMode.NORMAL.value,
            CH.DAC2.value: PowerMode.NORMAL.value,
            CH.DAC1.value: PowerMode.NORMAL.value,
            CH.DAC0.value: PowerMode.NORMAL.value,
        }

    def __send_to_gpio_pins(self, analog_out: int, voltage: float):
        ao_pin = self.__analog_out_pin_map[analog_out].value

        if voltage > 0:
            self.gpio.set_expander_pin(ao_pin)
        elif voltage == 0:
            self.gpio.clear_expander_pin(ao_pin)
        else:
            raise ValueError("voltage cannot be negative")

    # TODO: Decimal instead of float for precision testing
    def write_voltage(self, analog_out: int, voltage: float):
        """
        Write a voltage value to an analog out pin. Voltage will be continuously
        transmitted throught the analog out pin until a 0 V value is written to it.

        Args:
            analog_out (int): A/D_OUT pin number to write a voltage value to.
                For example, to write to A/D_OUT1, set this parameter to 1.

            voltage (float): the voltage value to write, in volts.

        Raises:
            ValueError: if voltage has more decimal places than DAC accuracy limit
        """
        self.dac_ops.check_range(analog_out, 1, NUM_PINS)
        self.dac_ops.check_range(voltage, 0, UPPER_LIMIT)
        dac_ch = self.__analog_out_to_dac_ch[analog_out]
        code = self.dac_ops.voltage_to_code(dac_ch, voltage)
        print(code)
        # update DAC register
        self.transfer(self.dac_ops.generate_write_and_update_command(dac_ch, code))
        # send voltage to analog out pin
        self.__send_to_gpio_pins(analog_out, voltage)
        return code

    def set_power_mode(self, analog_out: int, power_mode: PowerMode):
        """
        Set power mode for individual DAC channels to either normal power consumption,
        or low power consumption modes.

        For example, this may be of use when no constant power source available.

        Args:
            analog_out (int): the analog out pin whose power mode will be changed

            power_mode (PowerMode): a valid hex code for setting DAC channel power mode
        """
        self.dac_ops.check_range(analog_out, 1, NUM_PINS)
        dac_ch = self.__analog_out_to_dac_ch[analog_out]
        self.__dac_power_state[dac_ch] = power_mode.value
        power_code = self.dac_ops.generate_power_code(self.__dac_power_state.values())
        cmd = self.dac_ops.combine_command(COM.COM_POWER_DOWN_OP.value, NULL_BITS, power_code)
        self.transfer(cmd)

    def reset(self):
        """
        Performs a software reset of the EdgePi DAC to power-on default values,
        and stops all voltage transmissions through pins.
        """
        cmd = self.dac_ops.combine_command(COM.COM_SW_RESET.value, NULL_BITS, SW_RESET)
        self.transfer(cmd)
        # return gpio pins to low
        self.gpio.set_expander_default()

    def compute_expected_voltage(self, analog_out: int) -> float:
        """
        Computes expected voltage from the DAC channel corresponding to analog out pin.
        This is not guaranteed to be the voltage of the analog_out pin at the terminal block,
        nor the voltage being output by the DAC channel. It is a calculation that maps
        the contents of the DAC channel to a voltage value.

        Args:
            analog_out (int): the analog out pin number to read voltage from

        Returns:
            float: the computed voltage value of the DAC channel corresponding
                to the selected analog out pin.
        """
        self.dac_ops.check_range(analog_out, 1, NUM_PINS)
        dac_ch = self.__analog_out_to_dac_ch[analog_out]
        # first transfer triggers read mode, second is needed to fetch data
        cmd = self.dac_ops.combine_command(COM.COM_READBACK.value, CH(dac_ch).value, NULL_BITS)
        self.transfer(cmd)
        # all zero dummy command to trigger second transfer which
        # contains the DAC register contents.
        read_data = self.transfer([NULL_BITS, NULL_BITS, NULL_BITS])
        _logger.debug(f"reading code {read_data}")
        code = self.dac_ops.extract_read_data(read_data)
        return self.dac_ops.code_to_voltage(dac_ch, code)
