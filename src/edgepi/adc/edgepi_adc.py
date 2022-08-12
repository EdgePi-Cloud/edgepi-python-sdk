""" User interface for EdgePi ADC """


import logging

import bitstring
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
from edgepi.reg_helper.reg_helper import OpCode, BitMask


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

        Returns:
            `list`: a list of integer byte values formatted as
                [null_byte, null_byte, reg_1_data, reg_2_data,...] where reg_1_data
                is the data of the register at start_addx.
        """
        if num_regs < 1:
            raise ValueError("number of registers to read must be at least 1")
        code = self.adc_ops.read_register_command(start_addx.value, num_regs)
        _logger.debug(f"ADC __read_register -> data in: {code}")
        out = self.transfer(code)
        _logger.debug(f"ADC __read_register -> data out: {out}")
        return out

    def __write_register(self, start_addx: ADCReg, data: list[int]):
        """
        Write data to ADC registers, either individually or as a block.

        Args:
            `start_addx` (ADCReg): address of register to start writing data from.

            `data`: list of int values, where each value represents a byte of data
                to write to a register.
        """
        if len(data) < 1:
            raise ValueError("number of registers to write to must be at least 1")
        code = self.adc_ops.write_register_command(start_addx.value, data)
        _logger.debug(f"ADC __write_register -> data in: {code}")
        out = self.transfer(code)
        _logger.debug(f"ADC __write_register -> data out: {out}")
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

    @staticmethod
    def __get_channel_assign_opcodes(
        adc_1_mux_p=None, adc_2_mux_p=None, adc_1_mux_n=None, adc_2_mux_n=None
    ):
        """
        Generates OpCodes for assigning positive and negative multiplexers
        of either ADC1 or ADC2 to an ADC input channel.

        Returns:
            `generator`: if not empty, contains OpCode(s) for updating multiplexer
                channel assignment for ADC1, ADC2, or both.
        """
        if adc_1_mux_p is not None and adc_1_mux_p == adc_2_mux_p:
            raise ChannelMappingError("ADC1 and ADC2 must be assigned different input channels")

        adc_mux_regs = {
            ADCReg.REG_INPMUX: (adc_1_mux_p, adc_1_mux_n),
            ADCReg.REG_ADC2MUX: (adc_2_mux_p, adc_2_mux_n),
        }

        for addx, byte in adc_mux_regs.items():
            mux_p = byte[0]
            mux_n = byte[1]

            # not updating mux's for this adc_num (no args passed)
            if mux_p is None and mux_n is None:
                continue
            # updating mux_p bits only, mask mux_p bits
            elif mux_n is None:
                mask = BitMask.HIGH_NIBBLE
                # replace None with 0 for building bitstring
                mux_n = 0
            # updating mux_n bits only, mask mux_n bits
            elif mux_p is None:
                mask = BitMask.LOW_NIBBLE
                # replace None with 0 for building bitstring
                mux_p = 0
            # updating both mux_n and mux_p
            else:
                mask = BitMask.BYTE

            adc_x_ch_bits = bitstring.pack("uint:4, uint:4", mux_p, mux_n).uint

            yield OpCode(adc_x_ch_bits, addx.value, mask.value)

    def __config(
        self,
        adc1_ch: ADCChannel = None,
        adc2_ch: ADCChannel = None,
        adc1_data_rate: ADC1DataRate = None,
        adc2_data_rate: ADC2DataRate = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
        checksum_mode=None,
        gain=None,
    ):
        """
        Configure all ADC settings, either collectively or individually.
        Warning: users should only use set_config for modifying settings.
        """

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
        Configure user accessible ADC settings, either collectively or individually.

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
        # TODO: get dict of args, pass to __config
