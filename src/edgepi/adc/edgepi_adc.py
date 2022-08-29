""" User interface for EdgePi ADC """


from enum import Enum
import logging
import time

from bitstring import pack
from edgepi.peripherals.spi import SpiDevice as SPI
from edgepi.adc.adc_commands import ADCCommands
from edgepi.adc.adc_constants import (
    ADC1DataRate,
    ADC2DataRate,
    ADCChannel as CH,
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
from edgepi.adc.adc_multiplexers import (
    generate_mux_opcodes,
    ChannelMappingError,
    validate_channels_set,
    validate_channels_allowed,
)


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
        # configure ADC1 -> MUXP = floating, MUXN = AINCOM
        self.__config(adc_1_analog_in=CH.FLOAT, adc_1_mux_n=CH.AINCOM)
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

    def stop_auto_conversions(self):
        """
        Halt voltage read conversions when ADC is set to perform continuous conversions
        """
        # TODO: convert to parameter when ADC2 added
        adc = ADCNum.ADC_1.value
        self.transfer([adc.stop_cmd])

    def start_auto_conversions(self):
        """
        Start voltage read conversions when ADC is set to perform continuous conversions.
        The read data can be retrieved via the `read_voltage` method.
        """
        # TODO: convert to parameter when ADC2 added
        adc = ADCNum.ADC_1.value
        self.transfer([adc.start_cmd])

    def __is_in_pulse_mode(self):
        """Returns true if ADC1 is in pulse conversion mode else false"""
        mode_0 = pack("uint:8", self.__read_register(ADCReg.REG_MODE0)[0])
        return mode_0[1] is True

    def __get_data_read_len(self):
        read_config = pack("uint:8", self.__read_register(ADCReg.REG_INTERFACE)[0])

        # basic read length: 4 data bytes (adc1) or 3 data bytes + 1 zeros byte (adc2)
        read_bytes = 4

        # checksum byte enabled?
        if read_config[6:8].uint != 0x0:
            read_bytes += 1
        # status byte enabled?
        read_bytes += int(read_config[5])

        return read_bytes

    def read_voltage(self):
        """
        Read input voltage from selected ADC

        Args:
            `adc` (ADCNum): the ADC from which to read input voltage

        returns:
            `float`: input voltage read from ADC
        """
        # TODO: when ADC2 functionality is needed, convert this to parameter.
        adc = ADCNum.ADC_1

        # assert this adc not set to float mode
        mux_reg_val = self.__read_register(adc.value.addx)[0]
        validate_channels_set(mux_reg_val)

        # if reading adc1 and in pulse conversion mode, send start cmd
        if adc.value.id_num == 1 and self.__is_in_pulse_mode():
            self.transfer([adc.value.start_cmd])

        # TODO: compute delay based on settings
        time.sleep(0.5)

        # read value stored in this ADC's data holding register
        num_bytes = self.__get_data_read_len()
        read_data = self.transfer([adc.value.read_cmd] + [255] * num_bytes)

        # TODO: convert read_data from code to voltage

        return read_data

    def read_adc1_alarms(self):
        """
        Read ADC1 output faults

        Returns:
            `dict`: a dictionary of ADCAlarmType: ADCAlarm entries
        """
        raise NotImplementedError

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

    def __get_rtd_en_status(self):
        idac_mag = pack("uint:8", self.__read_register(ADCReg.REG_IDACMAG)[0])
        idac_1 = idac_mag[4:].uint
        return idac_1 == 0x0

    def __get_channel_assign_opcodes(
        self,
        adc_1_mux_p: CH = None,
        adc_2_mux_p: CH = None,
        adc_1_mux_n: CH = None,
        adc_2_mux_n: CH = None,
    ):
        """
        Generates OpCodes for assigning positive and negative multiplexers
        of either ADC1 or ADC2 to an ADC input channel. This is needed to allow
        users to assign multiplexers by input channel number.

        Args:
            adc_1_mux_p: input channel to assign to MUXP of ADC1
            adc_2_mux_p: input channel to assign to MUXP of ADC2
            adc_1_mux_n: input channel to assign to MUXN of ADC1
            adc_2_mux_n: input channel to assign to MUXN of ADC2

        Returns:
            `list`: if not empty, contains OpCode(s) for updating multiplexer
                channel assignment for ADC1, ADC2, or both.

        Raises:
            `ChannelMappingError`: if args assign any two multiplexers to the same input channel
        """
        args = filter_dict(locals(), "self")

        # no multiplexer config to update
        if all(x is None for x in list(args.values())):
            return []

        # allowed channels depend on RTD_EN status
        channels = filter(lambda x: x is not None, args.values())
        rtd_enabled = self.__get_rtd_en_status()
        validate_channels_allowed(channels, rtd_enabled)

        if len(args) != len(set(args)):
            raise ChannelMappingError(
                "ADC1 and ADC2 multiplexers must be assigned different input channels"
            )

        adc_mux_updates = {
            ADCReg.REG_INPMUX: (adc_1_mux_p, adc_1_mux_n),
            ADCReg.REG_ADC2MUX: (adc_2_mux_p, adc_2_mux_n),
        }

        # get mux register values for mux_mapping validation
        adc_1_mux_val = pack("uint:8", self.__read_register(ADCReg.REG_INPMUX)[0])
        adc_2_mux_val = pack("uint:8", self.__read_register(ADCReg.REG_ADC2MUX)[0])

        # current mux_mapping (for validating no duplicate channel assignment)
        mux_reg_vals = {
            ADCReg.REG_INPMUX: [adc_1_mux_val[:4].uint, adc_1_mux_val[4:].uint],
            ADCReg.REG_ADC2MUX: [adc_2_mux_val[:4].uint, adc_2_mux_val[4:].uint],
        }

        return generate_mux_opcodes(adc_mux_updates, mux_reg_vals)

    def __config(
        self,
        adc_1_analog_in: CH = None,
        adc_2_analog_in: CH = None,
        adc_1_mux_n: CH = None,
        adc_2_mux_n: CH = None,
        adc_1_data_rate: ADC1DataRate = None,
        adc_2_data_rate: ADC2DataRate = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
        checksum_mode=None,
        gain=None,
    ):
        """
        Configure all ADC settings, either collectively or individually.
        Warning: for developers only, users should use set_config for modifying settings.

        Args:
            `adc_1_analog_in` (ADCChannel): input voltage channel to map to ADC1 mux_p
            `adc_2_analog_in` (ADCChannel): input voltage channel to map to ADC2 mux_p
            'adc_1_mux_n` (ADCChannel): input voltage channel to map to ADC1 mux_n
            'adc_2_mux_n` (ADCChannel): input voltage channel to map to ADC1 mux_n
            `adc_1_data_rate` (ADC1DataRate): ADC1 data rate in samples per second
            `adc_2_data_rate` (ADC2DataRate): ADC2 data rate in samples per second,
            `filter_mode` (FilterMode): filter mode for both ADC1 and ADC2.
                Note this affects data rate. Please refer to module documentation
                for more information.
            `conversion_mode` (ConvMode): set conversion mode for ADC1.
                Note, ADC2 runs only in continuous conversion mode.
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
        mux_opcodes = self.__get_channel_assign_opcodes(
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
        data = [entry["value"] for entry in reg_values.values()]
        self.__write_register(ADCReg.REG_ID, data)

        return reg_values

    def set_config(
        self,
        adc_1_analog_in: CH = None,
        adc_1_data_rate: ADC1DataRate = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
    ):
        """
        Configure user accessible ADC settings, either collectively or individually.

        Args:
            `adc_1_analog_in` (ADCChannel): the input voltage channel to measure via ADC1
            `adc_1_data_rate` (ADC1DataRate): ADC1 data rate in samples per second
            `filter_mode` (FilterMode): filter mode for ADC1.
                Note this affects data rate. Please refer to module documentation
                for more information.
            `conversion_mode` (ConvMode): set conversion mode for ADC1.
        """
        # pylint: disable=unused-argument

        args = filter_dict(locals(), "self", None)
        self.__config(**args)
