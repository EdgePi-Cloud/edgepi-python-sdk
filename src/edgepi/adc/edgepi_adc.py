""" User interface for EdgePi ADC """


from enum import Enum
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
    ADC_NUM_REGS,
)
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.gpio_configs import GpioConfigs
from edgepi.utilities.utilities import filter_dict
from edgepi.reg_helper.reg_helper import OpCode, apply_opcodes


_logger = logging.getLogger(__name__)


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
        # first 2 entries are null bytes
        return out[2:]

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

    def __read_registers_to_map(self):
        """
        Reads value of all ADC registers

        Returns:
            `dict`: contains (register addx (int): register_value (int)) pairs
        """
        # get register values
        reg_values = self.__read_register(ADCReg.REG_ID, ADC_NUM_REGS)
        addx = ADCReg.REG_ID.value

        # Build dict with (register addx : register_value) pairs.
        reg_dict = {addx + i: reg_values[i] for i in range(ADC_NUM_REGS)}
        _logger.debug(f"__read_registers_to_map: {reg_dict}")

        return reg_dict

    def __config(
        self,
        adc_1_analog_in: ADCChannel = None,
        adc_2_analog_in: ADCChannel = None,
        adc_1_mux_n: ADCChannel = None,
        adc_2_mux_n: ADCChannel = None,
        adc1_data_rate: ADC1DataRate = None,
        adc2_data_rate: ADC2DataRate = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
        checksum_mode=None,
        gain=None,
    ):
        """
        Configure all ADC settings, either collectively or individually.
        Warning: for developers only, users should use set_config for modifying settings.
        """
        # pylint: disable=unused-argument

        # filter out self and None args
        args = list(filter_dict(locals(), "self", None).values())
        _logger.debug(f"set_config: args dict after filter:\n\n {args}\n\n")

        # extract OpCode type args, since args may contain non-OpCode args
        ops_list = [
            entry.value
            for entry in args
            if issubclass(entry.__class__, Enum) and isinstance(entry.value, OpCode)
        ]

        # get opcodes for mapping multiplexers
        mux_opcodes = self.adc_ops.get_channel_assign_opcodes(
            adc_1_analog_in, adc_2_analog_in, adc_1_mux_n, adc_2_mux_n
        )
        ops_list += mux_opcodes

        # get current register values
        reg_values = self.__read_registers_to_map()
        _logger.debug(f"set_config: register values before updates:\n\n{reg_values}\n\n")

        # get codes to update register values
        apply_opcodes(reg_values, ops_list)
        _logger.debug(f"set_config: register values after updates:\n\n{reg_values}\n\n")

        # write updated reg values to ADC using a single write.
        data = [ entry["value"] for entry in reg_values.values() ]
        self.__write_register(ADCReg.REG_ID, data)

        return reg_values

    def set_config(
        self,
        adc_1_analog_in: ADCChannel = None,
        adc_2_analog_in: ADCChannel = None,
        adc1_data_rate: ADC1DataRate = None,
        adc2_data_rate: ADC2DataRate = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
    ):
        """
        Configure user accessible ADC settings, either collectively or individually.

        Args:
            `adc_1_analog_in` (ADCChannel): the input voltage channel to measure via ADC1
            `adc_1_analog_in` (ADCChannel): the input voltage channel to measure via ADC2
            `adc1_data_rate` (ADCDataRate1): ADC1 data rate in samples per second
            `adc2_data_rate` (ADC2DataRate): ADC2 data rate in samples per second,
            `filter_mode` (FilterMode): filter mode for both ADC1 and ADC2.
                Note this affects data rate. Please refer to module documentation
                for more information.
            `conversion_mode` (ConvMode): set conversion mode for ADC1.
                Note, ADC2 runs only in continuous conversion mode.
        """
        args = filter_dict(locals(), "self", None)
        self.__config(**args)
