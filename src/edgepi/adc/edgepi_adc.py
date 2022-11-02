""" User interface for EdgePi ADC """


from dataclasses import dataclass
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
    ADCReferenceSwitching,
    ADC_NUM_REGS,
    ADC_VOLTAGE_READ_LEN,
    CheckMode,
    ADCModes,
    DifferentialPair,
)
from edgepi.adc.adc_voltage import code_to_voltage, check_crc
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.gpio_configs import GpioConfigs, ADCPins
from edgepi.utilities.utilities import filter_dict
from edgepi.reg_helper.reg_helper import OpCode, apply_opcodes
from edgepi.adc.adc_multiplexers import (
    generate_mux_opcodes,
    validate_channels_allowed,
)
from edgepi.adc.adc_conv_time import expected_initial_time_delay, expected_continuous_time_delay
from edgepi.adc.adc_status import get_adc_status

_logger = logging.getLogger(__name__)


@dataclass
class ADCState:
    """Represents ADC register states"""

    reg_map: dict  # map of most recently updated register values

    def get_state(self, mode: ADCModes) -> int:
        """
        Get state of an ADC functional mode based on most recently updated register values.
        Requires a call to __config() after ADC has been instantiated, before calling this. 

        This returns the op_code value used to set this functional mode.
        For example, ConvMode.PULSE uses an op_code value of `0x40`. If the current
        ADC state indicates conversion mode is ConvMode.PULSE and mode=ADCModes.CONV,
        this will return `0x40`, which can then be compared to `ConvMode.PULSE.value.op_code`
        to check if the ADC's conversion mode is set to `PULSE`.

        Args:
            `mode` (ADCModes): addx and mask used for this functional mode.

        Returns:
            `int`: uint value of the bits corresponding to this functional mode. Compare
                this to expected configuration's op_code.
        """
        if self.reg_map is None:
            raise ADCStateMissingMap("ADCState has not been assigned a register map")
        # register value at this addx
        reg_value = self.reg_map[mode.value.addx]["value"]
        # get op_code corresponding to this mode by letting through only "masked" bits
        mode_bits = (~mode.value.mask) & reg_value
        _logger.debug(f"ADCMode={mode}, value of mode bits = {hex(mode_bits)}")
        return mode_bits


class ADCStateMissingMap(Exception):
    """"Raised if ADCState.get_state() is called before ADCState.reg_map is assigned a value"""


class ADCRegisterUpdateError(Exception):
    """Raised when a register update fails to set register to expected value"""


class VoltageReadError(Exception):
    """Raised if a voltage read fails to return the expected number of bytes"""


class ContinuousModeError(Exception):
    """Raised when `read_voltage` is called and ADC is not in CONTINUOUS conversion mode"""


class RTDEnabledError(Exception):
    """Raised when user attempts to set ADC configuration that conflicts with RTD mode"""


class EdgePiADC(SPI):
    """EdgePi ADC device"""

    def __init__(self):
        super().__init__(bus_num=6, dev_id=1)
        self.adc_ops = ADCCommands()
        self.gpio = EdgePiGPIO(GpioConfigs.ADC.value)
        # internal state
        self.__state = ADCState(reg_map=None)
        # TODO: remove this from init(), rename to reset_config, after init call reset onfig to
        # reset registers.
        self.__set_power_on_configs()
        # TODO: adc reference should ba a config that customer passes depending on the range of
        # voltage they are measuring. To be changed later when range config is implemented
        self.set_adc_reference(ADCReferenceSwitching.GND_SW1.value)
        # TODO: get gain, offset, ref configs from the config module

    def __set_power_on_configs(self):
        """Custom EdgePi ADC configuration for initialization/reset"""
        self.__config(
            # TODO: this is also problematic, chainging the state when another module is working
            adc_1_analog_in=CH.AIN0,
            adc_1_mux_n=CH.AINCOM,
            checksum_mode=CheckMode.CHECK_BYTE_CRC,
            # TODO: have a manual function to clear the reset bit.
            reset_clear=ADCPower.RESET_CLEAR,
        )

    def __read_register(self, start_addx: ADCReg, num_regs: int = 1):
        """
        Read data from ADC registers, either individually or as a block.

        Args:
            `start_addx` (ADCReg): address of register to start read at.

            `num_regs` (int): number of registers to read from start_addx, including
                start_addx register.

        Returns:
            `list`: a list of ints representing bytes formatted as [reg_1_data, reg_2_data,...]
                where reg_1_data is the data of the register at start_addx.
        """
        if num_regs < 1:
            raise ValueError("Number of registers to read must be at least 1")

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

            `data` (list): list of int values, where each value represents a byte of data
                to write to a register.
        """
        if len(data) < 1:
            raise ValueError("Number of registers to write to must be at least 1")

        code = self.adc_ops.write_register_command(start_addx.value, data)
        _logger.debug(f"ADC __write_register -> data in: {code}")
        out = self.transfer(code)
        _logger.debug(f"ADC __write_register -> data out: {out}")

        return out

    def set_adc_reference(self, reference_config: ADCReferenceSwitching = None):
        """
        Setting ADC referene terminal state. pin 18 and 23 labeled IN GND on the enclosure. It can
        be configured as regular 0V GND or 12V GND.

        Args:
            reference_config: (ADCReferenceSwitching): selecting none, 1, 2, both
        """
        if reference_config == ADCReferenceSwitching.GND_SW1.value:
            self.gpio.set_expander_pin(ADCPins.GNDSW_IN1.value)
            self.gpio.clear_expander_pin(ADCPins.GNDSW_IN2.value)
        elif reference_config == ADCReferenceSwitching.GND_SW2.value:
            self.gpio.set_expander_pin(ADCPins.GNDSW_IN2.value)
            self.gpio.clear_expander_pin(ADCPins.GNDSW_IN1.value)
        elif reference_config == ADCReferenceSwitching.GND_SW_BOTH.value:
            self.gpio.set_expander_pin(ADCPins.GNDSW_IN1.value)
            self.gpio.set_expander_pin(ADCPins.GNDSW_IN2.value)
        elif reference_config == ADCReferenceSwitching.GND_SW_NONE.value:
            self.gpio.clear_expander_pin(ADCPins.GNDSW_IN1.value)
            self.gpio.clear_expander_pin(ADCPins.GNDSW_IN2.value)

    def stop_conversions(self):
        """
        Halt voltage read conversions when ADC is set to perform continuous conversions
        """
        # TODO: convert adc_num to parameter when ADC2 added
        adc = ADCNum.ADC_1
        stop_cmd = self.adc_ops.stop_adc(adc_num=adc.value)
        self.transfer(stop_cmd)

    def __send_start_command(self, adc_num):
        """Triggers ADC conversion(s)"""
        start_cmd = self.adc_ops.start_adc(adc_num=adc_num.value)
        self.transfer(start_cmd)

    def start_conversions(self):
        """
        Start ADC voltage read conversions. If ADC is continuous conversion mode,
        this method must be called before performing reads. If ADC is in
        pulse conversion mode, this method does not need to be called before
        performing reads.
        """
        # TODO: convert adc_num to parameter when ADC2 added
        adc_num = ADCNum.ADC_1

        # get state for configs relevant to conversion delay
        conv_mode = self.__state.get_state(ADCModes.CONV)
        data_rate = (
            self.__state.get_state(ADCModes.DATA_RATE_1)
            if adc_num == ADCNum.ADC_1
            else self.__state.get_state(ADCModes.DATA_RATE_2)
        )
        filter_mode = self.__state.get_state(ADCModes.FILTER)

        conv_delay = expected_initial_time_delay(adc_num, data_rate, filter_mode)
        _logger.debug(
            (
                f"\nComputed time delay = {conv_delay} (ms) with the following config opcodes:\n"
                f"adc_num={adc_num}, conv_mode={hex(conv_mode)}, "
                f"data_rate={hex(data_rate)} filter_mode={hex(filter_mode)}\n"
            )
        )
        self.__send_start_command(adc_num)

        # apply delay for first conversion
        time.sleep(conv_delay / 1000)

    def clear_reset_bit(self):
        """
        Clear the ADC RESET bit of POWER register, in order to enable detecting
        new ADC resets through the STATUS byte of a voltage read.
        """
        self.__config(reset_clear=ADCPower.RESET_CLEAR)

    def __read_data(self, adc: ADCNum, data_size: int):
        """Sends command to ADC to get new voltage conversion data"""
        return self.transfer([adc.value.read_cmd] + [255] * data_size)

    def __voltage_read(self, adc):
        """
        Performs ADC voltage read and formats output into status, voltage,
        and check bytes

        Returns:
            (int): uint values of representations of voltage read data ordered as
                (status_byte, voltage_data_bytes, check_byte)
        """
        read_data = self.__read_data(adc, ADC_VOLTAGE_READ_LEN)

        if len(read_data) - 1 != ADC_VOLTAGE_READ_LEN:
            raise VoltageReadError(
                f"Voltage read failed: incorrect number of bytes ({len(read_data)}) retrieved"
            )

        status_code = read_data[1]

        voltage_code = read_data[2 : (2 + adc.value.num_data_bytes)]

        check_code = read_data[6]

        return status_code, voltage_code, check_code

    def read_voltage(self):
        """
        Read voltage from the currently configured ADC analog input channel.
        Use this method when ADC is configured to `CONTINUOUS` conversion mode.
        For `PULSE` conversion mode, use `single_sample()` instead.

        Returns:
            `float`: input voltage read from ADC
        """
        # TODO: when ADC2 functionality is added, convert this to parameter.
        adc = ADCNum.ADC_1

        # assert adc is in continuous mode (use ADCStatus)
        if self.__state.get_state(ADCModes.CONV) != ConvMode.CONTINUOUS.value.op_code:
            raise ContinuousModeError(
                "ADC must be in CONTINUOUS conversion mode in order to call `read_voltage`."
            )

        # get continuous mode time delay and wait here (delay is needed between each conversion)
        data_rate = (
            self.__state.get_state(ADCModes.DATA_RATE_1)
            if adc == ADCNum.ADC_1
            else self.__state.get_state(ADCModes.DATA_RATE_2)
        )
        delay = expected_continuous_time_delay(adc, data_rate)
        _logger.debug(
            (
                f"\nContinuous time delay = {delay} (ms) with the following config opcodes:\n"
                f"adc_num={adc},  data_rate={hex(data_rate)}\n"
            )
        )
        time.sleep(delay / 1000)

        status_code, voltage_code, check_code = self.__voltage_read(adc)

        # log STATUS byte
        status = get_adc_status(status_code)
        _logger.debug(f"Logging STATUS byte:\n{status}")

        # check CRC
        check_crc(voltage_code, check_code)

        # convert voltage_bits from code to voltage
        voltage = code_to_voltage(voltage_code, adc.value)

        return voltage

    def single_sample(self):
        """
        Perform a single `ADC1` voltage read in `PULSE` conversion mode.
        Do not call this method for voltage reading if ADC is configured
        to `CONTINUOUS` conversion mode: use `read_voltage` instead.
        """
        # assert adc is in PULSE mode (check ADCState) -> set to PULSE if not
        if self.__state.get_state(ADCModes.CONV) != ConvMode.PULSE.value.op_code:
            self.__config(conversion_mode=ConvMode.PULSE)

        # only ADC1 can perform PULSE conversion
        adc = ADCNum.ADC_1

        # send command to trigger conversion
        # TODO: pass in adc_num once ADC2 functionality is added
        self.start_conversions()

        # send command to read conversion data.
        status_code, voltage_code, check_code = self.__voltage_read(adc)

        # log STATUS byte
        status = get_adc_status(status_code)
        _logger.debug(f"Logging STATUS byte:\n{status}")

        # check CRC
        check_crc(voltage_code, check_code)

        # convert read_data from code to voltage
        voltage = code_to_voltage(voltage_code, adc.value)

        return voltage

    def reset(self):
        """
        Reset ADC register values to EdgePi ADC power-on state.
        Note this state differs from ADS1263 default power-on, due to
        application of custom power-on configuration required by EdgePi.
        """
        self.transfer(self.adc_ops.reset_adc())
        self.__set_power_on_configs()

    def __is_data_ready(self):
        # pylint: disable=unused-private-member
        # required for integration testing in test_conversion_times.py
        """Utility for testing conversion times, returns True if ADC indicates new voltage data"""
        read_data = self.transfer([ADCComs.COM_RDATA1.value] + [255] * 6)
        return read_data[1] & 0b01000000

    def __read_registers_to_map(self):
        """
        Reads value of all ADC registers to a dictionary

        Returns:
            `dict`: contains {register addx (int): register_value (int)} pairs
        """
        # get register values
        reg_values = self.__read_register(ADCReg.REG_ID, ADC_NUM_REGS)
        addx = ADCReg.REG_ID.value

        # build dict with (register addx : register_value) pairs.
        reg_dict = {addx + i: reg_values[i] for i in range(ADC_NUM_REGS)}
        _logger.debug(f"__read_registers_to_map: {reg_dict}")

        return reg_dict

    def __get_rtd_en_status(self):
        """
        Get state of RTD_EN pin (on/off), to use for deciding which
        ADC channels are available for reading.

        Returns:
            `bool`: True if RTD_EN pin is on, False otherwise
        """
        _logger.debug("Checking RTD status")
        idac_mag = pack("uint:8", self.__read_register(ADCReg.REG_IDACMAG)[0])
        idac_1 = idac_mag[4:].uint
        # TODO: this should be updated to check all RTD properties not just this one
        status = idac_1 != 0x0
        _logger.debug(f"RTD enabled: {status}")
        return status

    # TODO: is this really needed? Refactor to use predefined opcodes?
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
        """
        args = filter_dict(locals(), "self")

        # no multiplexer config to update
        if all(x is None for x in list(args.values())):
            return []

        # allowed channels depend on RTD_EN status
        channels = list(filter(lambda x: x is not None, args.values()))
        rtd_enabled = self.__get_rtd_en_status()
        validate_channels_allowed(channels, rtd_enabled)

        adc_mux_updates = {
            ADCReg.REG_INPMUX: (adc_1_mux_p, adc_1_mux_n),
            ADCReg.REG_ADC2MUX: (adc_2_mux_p, adc_2_mux_n),
        }

        return generate_mux_opcodes(adc_mux_updates)

    def select_differential(self, adc: ADCNum, diff_mode: DifferentialPair):
        """
        Select a differential voltage sampling mode for either ADC1 or ADC2

        Args:
            `adc` (ADCNum): identity of ADC to configure

            `diff_mode` (DifferentialPair): a pair of input channels to sample, or off

        Raises:
            `KeyError`: if adc is not a valid ADCNum enum
        """
        mux_p = diff_mode.value.mux_p
        mux_n = diff_mode.value.mux_n
        mux_properties = {
            ADCNum.ADC_1: {
                'adc_1_analog_in': mux_p,
                'adc_1_mux_n': mux_n,
            },
            ADCNum.ADC_2: {
                'adc_2_analog_in': mux_p,
                'adc_2_mux_n': mux_n,
            }
        }
        diff_update = mux_properties[adc]
        self.__config(**diff_update)

    def __validate_no_rtd_conflict(self, updates: dict):
        """
        Checks no RTD related properties are being updated if RTD mode is enabled

        Args:
            `updates` (dict): updates formatted as {'property_name': update_value}

        Raises:
            `RTDEnabledError`: if RTD is enabled and an RTD related property is in updates
        """
        # ADC2 channel setting conflicts with RTD handled during channel mapping
        rtd_properties = {
            'adc_1_analog_in',
            'adc_1_mux_n',
            'idac_1_mux',
            'idac_2_mux',
            'idac_1_mag',
            'idac_2_mag',
            'pos_ref_inp',
            'neg_ref_inp'
        }
        is_rtd_on = self.__get_rtd_en_status()
        if not is_rtd_on:
            return

        for update in updates:
            if update in rtd_properties:
                raise RTDEnabledError(
                    f"ADC property '{update}' cannot be updated while RTD is enabled"
                )

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
        checksum_mode: CheckMode = None,
        reset_clear: ADCPower = None,
        validate: bool = True,
        idac_1_mux = None,
        idac_2_mux = None,
        idac_1_mag = None,
        idac_2_mag = None,
        pos_ref_inp = None,
        neg_ref_inp = None 
    ):
        """
        Configure all ADC settings, either collectively or individually.
        Warning: for internal EdgePi developer use only, users should use
        `set_config()` for modifying settings instead.

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
            `checksum_mode` (CheckMode): set mode for CHECK byte
            `reset_clear` (ADCPower): set state of ADC RESET bit
            `validate` (bool): set to True to perform post-update validation
            `idac_1_mux` (IDACMUX): set analog input pin to connect IDAC1
            `idac_2_mux` (IDACMUX): set analog input pin to connect IDAC2
            `idac_1_mag` (IDACMAG): set the current value for IDAC1
            `idac_2_mag` (IDACMAG): set the current value for IDAC2
            `pos_ref_inp` (REFMUX): set the positive reference input
            `neg_ref_inp` (REFMUX): set the negative reference input
        """
        # pylint: disable=unused-argument

        # filter out self and None args
        args = filter_dict(locals(), "self", None)
        self.__validate_no_rtd_conflict(args)
        args = list(args.values())
        _logger.debug(f"__config: args dict after filter:\n\n{args}\n\n")

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
        _logger.debug(f"__config: register values before updates:\n\n{reg_values}\n\n")

        # get codes to update register values
        apply_opcodes(reg_values, ops_list)
        _logger.debug(f"__config: register values after updates:\n\n{reg_values}\n\n")

        # write updated reg values to ADC using a single write.
        data = [entry["value"] for entry in reg_values.values()]
        self.__write_register(ADCReg.REG_ID, data)

        # validate updates were applied correctly
        if validate:
            self.__validate_updates(reg_values)

        # update ADC state
        self.__state.reg_map = reg_values

        return reg_values

    def __validate_updates(self, updated_reg_values: dict):
        """
        Validates updated config values have been applied to ADC registers.

        Args:
            updated_reg_values (dict): register values that were applied in latest __config()
        """
        reg_values = self.__read_registers_to_map()

        # check updated value were applied
        for addx, value in reg_values.items():
            observed_val = updated_reg_values[addx]["value"]
            if int(value) != int(updated_reg_values[addx]["value"]):
                _logger.error("__config: failed to update register")
                raise ADCRegisterUpdateError(
                    (
                        "Register failed to update: "
                        f"addx={hex(addx)}, expected: {hex(value)}, observed: {hex(observed_val)}"
                    )
                )

        return True

    def set_config(
        self,
        adc_1_analog_in: CH = None,
        adc_1_data_rate: ADC1DataRate = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
        validate: bool = True,
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
            `validate` (bool): set to False to skip update validation
        """
        # pylint: disable=unused-argument

        args = filter_dict(locals(), "self", None)
        self.__config(**args)
