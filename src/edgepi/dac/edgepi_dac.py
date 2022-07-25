"""
Module for interacting with the EdgePi DAC via SPI.
"""


import logging
from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_calibration import DAChWCalibConst, DACsWCalibConst
from edgepi.dac.dac_constants import (
    NULL_BITS,
    SW_RESET,
    DAC_PRECISION,
    PowerMode,
    EdgePiDacChannel as CH,
    EdgePiDacCom as COM,
    AOPins,
)
from edgepi.peripherals.spi import SpiDevice as spi
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.gpio_configs import GpioConfigs


_logger = logging.getLogger(__name__)

# TODO: map analog_out number to AO EN pins


class EdgePiDAC(spi):
    """A EdgePi DAC device"""

    __dac_pin_map = {
        1: AOPins.AO_EN1,
        2: AOPins.AO_EN2,
        3: AOPins.AO_EN3,
        4: AOPins.AO_EN4,
        5: AOPins.AO_EN5,
        6: AOPins.AO_EN6,
        7: AOPins.AO_EN7,
        8: AOPins.AO_EN8,
    }

    def __init__(self):
        _logger.info("Initializing DAC Bus")
        super().__init__(bus_num=6, dev_id=3, mode=1, max_speed=1000000)

        self.dac_ops = DACCommands(DAChWCalibConst, [DACsWCalibConst] * 8)
        self.gpio = EdgePiGPIO(GpioConfigs.DAC.value)
        self.gpio.set_expander_default()

        self._dac_power_state = {
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
        ao_pin = self.__dac_pin_map[analog_out].value

        if voltage > 0:
            self.gpio.set_expander_pin(ao_pin)
        else:
            self.gpio.clear_expander_pin(ao_pin)

    def write_voltage(self, analog_out: int, voltage: float):
        """
        Write a voltage value to an analog out pin. Voltage will be continuously
        transmitted throught he analog out pin until a 0 V value is written to it.

        Args:
            analog_out (int): A/D_OUT pin number to write a voltage value to.
                For example, to write to A/D_OUT1, set this parameter to 1.

            voltage (float): the voltage value to write, in volts.

        Raises:
            ValueError: if voltage has more decimal places than DAC accuracy limit
        """
        if not self.dac_ops.validate_voltage_precision(voltage):
            raise ValueError(f"DAC voltage writes currently support {DAC_PRECISION} decimal places")
        dac_ch = analog_out - 1
        code = self.dac_ops.voltage_to_code(dac_ch, voltage)
        # update DAC register
        self.transfer(self.dac_ops.generate_write_and_update_command(dac_ch, code))
        # send voltage to analog out pin
        self.__send_to_gpio_pins(analog_out, voltage)

    def set_power_mode(self, analog_out: int, power_mode: PowerMode):
        """
        Set power mode for individual DAC channels to either normal power consumption,
        or low power consumption modes.

        Args:
            analog_out (int): the analog out pin whose power mode will be changed

            power_mode (PowerMode): a valid hex code for setting DAC channel power mode
        """
        self.dac_ops.check_range(analog_out, 1, len(CH))
        dac_ch = analog_out - 1  # analog_out pins numbered 1-8, DAC channels 0-7
        self._dac_power_state[dac_ch] = power_mode.value
        power_code = self.dac_ops.generate_power_code(self._dac_power_state.values())
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

    def read_voltage(self, analog_out: int) -> float:
        """
        Read voltage from the DAC channel corresponding to analog out pin

        Args:
            analog_out (int): the analog out pin number to read voltage from

        Returns:
            float: the voltage value read from the DAC channel corresponding
                to the selected analog out pin.
        """
        self.dac_ops.check_range(analog_out, 1, len(CH))
        dac_ch = analog_out - 1
        # first transfer triggers read mode, second is needed to fetch data
        cmd = self.dac_ops.combine_command(COM.COM_READBACK.value, CH(dac_ch).value, NULL_BITS)
        self.transfer(cmd)
        # all zero dummy command to trigger second transfer which
        # contains the DAC register contents.
        read_data = self.transfer([NULL_BITS, NULL_BITS, NULL_BITS])
        _logger.debug(f"reading code {read_data}")
        code = self.dac_ops.extract_read_data(read_data)
        return self.dac_ops.code_to_voltage(dac_ch, code)
