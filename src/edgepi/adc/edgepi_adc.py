""" User interface for EdgePi ADC """


import logging

from edgepi.peripherals.spi import SpiDevice as SPI
from edgepi.adc.adc_commands import ADCCommands
from edgepi.adc.adc_constants import (
    ADC1DataRate,
    ADC2DataRate,
    ADCChannel,
    ADCNum,
    ConvMode,
    ADCReg,
    FilterMode,
)
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.gpio_configs import GpioConfigs
from edgepi.utilities.utilities import filter_dict


_logger = logging.getLogger(__name__)


class ChannelMappingError(ValueError):
    """Raised when an input channel is mapped to both ADC1 and ADC2"""


class EdgePiADC(SPI):
    """EdgePi ADC device"""

    def __init__(self):
        super().__init__(bus_num=6, dev_id=1)
        self.adc_ops = ADCCommands()
        self.gpio = EdgePiGPIO(GpioConfigs.ADC.value)
        self.gpio.set_expander_default()
        # TODO: non-user configs
        # - set gain
        # - MUXP = floating, MUXN = AINCOM
        # - enable CRC mode for checksum -> potentially will allow user
        #   to configure this in set_config if too much overhead.
        # - RTD off by default --> leave default settings for related regs

    def __read_register(self, start_addx: ADCReg, num_regs: int = 1):
        """
        Read data from ADC registers, either individually or as a block.

        Args:
            `start_addx` (ADCReg): address of register to start read at.

            `num_regs`: number of registers to read from start_addx, including
                start_addx register.
        """
        if num_regs < 1:
            raise ValueError("number of registers to read must be at least 1")
        code = self.adc_ops.read_register_command(start_addx.value, num_regs)
        _logger.debug(f"ADC __read_register -> data in: {code}")
        out = self.transfer(code)
        _logger.debug(f"ADC __read_register -> data out: {out}")
        return out

    def read_voltage(self, adc: ADCNum):
        """
        Read input voltage from selected ADC

        Args:
            `adc` (ADCNum): the ADC from which to read input voltage

        returns:
            `float`: input voltage read from ADC
        """
        # TODO: raise Exception if user performs read with MUXP = 0xF

    def read_adc1_alarms(self):
        """
        Read ADC1 output faults

        Returns:
            `dict`: a dictionary of ADCAlarmType: ADCAlarm entries
        """

    # TODO: optional -> def read_adc_data_status(self, ADCNum):

    def set_config(
        self,
        adc1_ch: ADCChannel = None,
        adc2_ch: ADCChannel = None,
        adc1_data_rate: ADC1DataRate = None,
        adc2_data_rate: ADC2DataRate = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
    ):
        """
        Configure ADC settings, either collectively or individually.

        Args:
            `adc1_ch` (ADCChannel): the input voltage channel to measure via ADC1
            `adc2_ch` (ADCChannel): the input voltage channel to measure via ADC2
            `adc1_data_rate` (ADCDataRate1): ADC1 data rate in samples per second
            `adc2_data_rate` (ADC2DataRate): ADC2 data rate in samples per second,
            `filter_mode` (FilterMode): filter mode for both ADC1 and ADC2.
                Note this affects data rate. Please refer to module documentation
                for more information.
            `conversion_mode` (ConvMode): set conversion mode for ADC1.
                Note, ADC2 runs only in continuous conversion mode.
        """
        if adc1_ch is not None and adc1_ch == adc2_ch:
            raise ChannelMappingError("ADC1 and ADC2 must be assigned different input channels")
