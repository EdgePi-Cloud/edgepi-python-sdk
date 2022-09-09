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
    ADCComs,
    ADCNum,
    ADCPower,
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
        # TODO: expander_pin might need changing in the future
        self.gpio.set_expander_pin("GNDSW_IN1")
        # TODO: non-user configs
        # - set gain
        self.__config(adc_1_analog_in=CH.FLOAT, adc_1_mux_n=CH.AINCOM)
        # TODO: - enable CRC mode for checksum -> potentially will allow user
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

    def stop_conversions(self):
        """
        Halt voltage read conversions when ADC is set to perform continuous conversions
        """
        # TODO: convert adc_num to parameter when ADC2 added
        adc = ADCNum.ADC_1.value
        self.transfer([adc.stop_cmd])

    def start_conversions(self):
        """
        Start voltage read conversions. If ADC is continuous conversion mode,
        this method must be called before performing reads. If ADC is in
        pulse conversion mode, this method does not need to be called before
        performing reads.
        """
        # TODO: convert adc_num to parameter when ADC2 added
        adc_num = ADCNum.ADC_1.value
        start_cmd = self.adc_ops.start_adc(adc_num=adc_num)
        self.transfer(start_cmd)
        # TODO: compute conversion time delay + wait here
        # - may not be needed for auto_mode though, include param
        # option to use time delay
        time.sleep(0.5)

    def __is_in_pulse_mode(self):
        """Returns true if ADC1 is in pulse conversion mode else false"""
        mode_0 = pack("uint:8", self.__read_register(ADCReg.REG_MODE0)[0])
        return mode_0[1] is True

    # TODO: refactor this to be simple bool check of params
    def __get_data_read_len(self, status_byte: bool, check_byte: bool = True):
        """
        Returns voltage read data frame size in bytes, depending on whether
        reads are currently configured to include the STATUS and CRC/CHK bytes
        """
        # basic read length: 4 data bytes (adc1), 3 data bytes + 1 null byte (adc2)
        read_bytes = 4

        return read_bytes + int(status_byte) + int(check_byte)

    def clear_reset_bit(self):
        """
        Clear the ADC RESET bit of POWER register, in order to enable detecting
        new ADC resets through the STATUS byte of a voltage read.
        """
        self.__config(reset_clear=ADCPower.RESET_CLEAR)

    def __read_data(self, adc: ADCNum, data_size: int):
        return self.transfer([adc.value.read_cmd] + [255] * data_size)

    def single_sample(self, status_byte: bool=False):
        """
        Perform a single ADC1 voltage read in PULSE conversion mode.
        Note, do not call this method for voltage reading if ADC is configured
        to CONTINUOUS conversion mode: use `read_voltage` instead.
        """
        self.start_conversions()

        num_bytes = self.__get_data_read_len(status_byte=status_byte)
        read_data = self.__read_data(adc=ADCNum.ADC_1, data_size=num_bytes)

        # TODO: check CRC
        # TODO: convert read_data from code to voltage

        return read_data


    def read_voltage(self):
        """
        Read input voltage from selected ADC

        Returns:
            `float`: input voltage read from ADC
        """
        # TODO: when ADC2 functionality is needed, convert this to parameter.
        adc = ADCNum.ADC_1

        # assert this adc not set to float mode
        # TODO: check if necessary: what happens if you read_voltage in floating mode
        # is the output garbage, and can you tell this from the data before conversion?
        # i.e. if data returned is garbage, then raise FloatMode error.
        # mux_reg_val = self.__read_register(adc.value.addx)[0]
        # validate_channels_set(mux_reg_val)

        # if reading adc1 and in pulse conversion mode, send start cmd
        # TODO: replace with adc == ADCNum.ADC_1
        # TODO: checking for pulse mode may conflict with high data rate
        # refactor to 2 functions to avoid calling read_register twice
        # or 1 function with passing in is_pulse_mode as boolean
        if adc.value.id_num == 1 and self.__is_in_pulse_mode():
            # TODO: call the helper function instead of rewriting here
            self.transfer([adc.value.start_cmd])

        # read value stored in this ADC's data holding register

        # TODO: refactor to private function that returns status, data, crc
        # with include status byte being optional
        # - enable crc byte by default in __init__, don't allow disabling it
        # - determine number of bytes based on parameter states
        # - only retrieve STATUS if parameter is TRUE to avoid register reading
        num_bytes = self.__get_data_read_len(True, True)
        read_data = self.transfer([adc.value.read_cmd] + [255] * num_bytes)

        # TODO: check CRC

        # TODO: convert read_data from code to voltage

        return read_data

    def is_data_ready(self):
        read_data = self.transfer([ADCComs.COM_RDATA1.value] + [255] * 6)
        # start = time.perf_counter_ns()
        # adc_1_bit = pack("uint:8", read_data[1])
        # adc_1_bit = read_data[1] & 0b01000000
        # end = time.perf_counter_ns()
        # print(f"pack time (ms): {(end-start)*10**-6}")
        return read_data[1] & 0b01000000

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
        channels = list(filter(lambda x: x is not None, args.values()))
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
        reset_clear: ADCPower = None,
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
