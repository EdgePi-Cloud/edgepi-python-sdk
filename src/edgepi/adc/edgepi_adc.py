""" User interface for EdgePi ADC """

from enum import Enum
from operator import attrgetter
import logging
import time

from edgepi.adc.adc_query_lang import PropertyValue
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.peripherals.spi import SpiDevice as SPI
from edgepi.adc.adc_commands import ADCCommands
from edgepi.adc.adc_constants import (
    ADC1PGA,
    ADC1DataRate,
    ADC2DataRate,
    ADCChannel as CH,
    ADCNum,
    ADCPower,
    ConvMode,
    ADCReg,
    DifferentialPair,
    FilterMode,
    ADCReferenceSwitching,
    ADC_NUM_REGS,
    ADC_VOLTAGE_READ_LEN,
    CheckMode,
    DiffMode,
    IDACMUX,
    IDACMAG,
    REFMUX,
    ADC2REFMUX,
    RTDModes,
    ADC1RtdConfig,
    ADC2RtdConfig,
    AllowedChannels,
    AnalogIn,
)
from edgepi.adc.adc_voltage import (
    code_to_voltage,
    code_to_temperature,
    code_to_voltage_single_ended
)
from edgepi.utilities.crc_8_atm import check_crc
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.gpio_configs import ADCPins, RTDPins
from edgepi.utilities.utilities import filter_dict, filter_dict_list_key_val
from edgepi.reg_helper.reg_helper import OpCode, apply_opcodes
from edgepi.adc.adc_multiplexers import (
    generate_mux_opcodes,
    validate_channels_allowed,
)
from edgepi.adc.adc_conv_time import expected_initial_time_delay, expected_continuous_time_delay
from edgepi.adc.adc_status import get_adc_status
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM
from edgepi.adc.adc_state import ADCState
from edgepi.adc.adc_exceptions import (
    ADCRegisterUpdateError,
    VoltageReadError,
    ContinuousModeError,
    RTDEnabledError,
    InvalidDifferentialPairError,
    CalibKeyMissingError
)

_logger = logging.getLogger(__name__)


class EdgePiADC(SPI):
    """
    EdgePi ADC device

    Warning, when caching is enabled to track the ADC's internal state, EdgePiADC objects are
    safe to use only within a single dev environment. Using multiple EdgePiADC objects,
    each within a different environment, will lead to the cached ADC state being out of sync
    with the actual hardware state. To avoid this, disable caching when creating the
    EdgePiADC object; the state of the ADC will be read from hardware instead, at the
    cost of increased SPI reading load.
    """

    # keep track of ADC register map state for state caching
    __state: dict = {}

    # default RTD model-dependent hardware constants
    RTD_SENSOR_RESISTANCE = 100 # RTD sensor resistance value (Ohms)
    RTD_SENSOR_RESISTANCE_VARIATION = 0.385 # RTD sensor resistance variation (Ohms/°C)

    __analog_in_to_adc_in_map = {
        AnalogIn.AIN1: CH.AIN0,
        AnalogIn.AIN2: CH.AIN1,
        AnalogIn.AIN3: CH.AIN2,
        AnalogIn.AIN4: CH.AIN3,
        AnalogIn.AIN5: CH.AIN4,
        AnalogIn.AIN6: CH.AIN5,
        AnalogIn.AIN7: CH.AIN6,
        AnalogIn.AIN8: CH.AIN7,
        AnalogIn.AINCOM : CH.AINCOM,
        AnalogIn.FLOAT : CH.FLOAT
    }

    def __init__(
        self,
        enable_cache: bool = False,
        rtd_sensor_resistance: float = None,
        rtd_sensor_resistance_variation: float = None
        ):
        """
        Args:
            `enable_cache` (bool): set to True to enable state-caching

            `rtd_sensor_resistance` (float): set RTD material-dependent resistance value (Ohms)

            `rtd_sensor_resistance_variation` (float): set RTD model-dependent resistance
                variation (Ohms/°C)
        """

        super().__init__(bus_num=6, dev_id=1)
        # declare instance vars before config call below
        self.enable_cache = enable_cache

        # Load eeprom data and generate dictionary of calibration dataclass
        eeprom = EdgePiEEPROM()
        eeprom_data  = eeprom.read_edgepi_data()
        self.adc_calib_params = {ADCNum.ADC_1:eeprom_data.adc1_calib_params.extract_ch_dict(),
                                 ADCNum.ADC_2:eeprom_data.adc2_calib_params.extract_ch_dict(),}
        self.rtd_calib = eeprom_data.rtd_calib_params

        self.adc_ops = ADCCommands()
        self.gpio = EdgePiGPIO()
        # ADC always needs to be in CRC check mode. This also updates the internal __state.
        # If this call to __config is removed, replace with a call to get_register_map to
        # initialize __state.
        self.__config(checksum_mode=CheckMode.CHECK_BYTE_CRC)
        # TODO: adc reference should ba a config that customer passes depending on the range of
        # voltage they are measuring. To be changed later when range config is implemented
        # self.set_adc_reference(ADCReferenceSwitching.GND_SW1.value)

        # user updated rtd hardware constants
        self.rtd_sensor_resistance = (
            rtd_sensor_resistance
            if rtd_sensor_resistance is not None
            else EdgePiADC.RTD_SENSOR_RESISTANCE
        )

        self.rtd_sensor_resistance_variation = (
            rtd_sensor_resistance_variation
            if rtd_sensor_resistance_variation is not None
            else EdgePiADC.RTD_SENSOR_RESISTANCE_VARIATION
        )

    def __reapply_config(self):
        """
        Restore ADC to custom EdgePi configuration
        """
        # turn RTD off to allow updates in case RTD is on
        self.set_rtd(set_rtd=False)
        self.__config(
            adc_1_ch=CH.FLOAT,
            adc_2_ch=CH.FLOAT,
            adc_1_mux_n=CH.AINCOM,
            adc_2_mux_n=CH.AINCOM,
            checksum_mode=CheckMode.CHECK_BYTE_CRC,
        )

    def __update_cache_map(self, reg_map: dict):
        """
        Format a register map to the same format as `read_registers_to_map` and
        assign to the internal ADC state.

        Args:
            `reg_map` (dict): register map formatted as {int: {"value": int}}
        """
        EdgePiADC.__state = {addx: entry["value"] for (addx, entry) in reg_map.items()}

    def __get_register_map(
        self,
        override_cache: bool = False,
    ) -> dict[int, int]:
        """
        Get a mapping of register addresses to register values, for the specified
        number of registers. All ADC methods which require register reading should
        call this method to get the register values.

        Args:
            `override_cache` (bool): force update cached state via SPI read

        Returns:
            dict: mapping of uint register addresses to uint register values
        """
        if not EdgePiADC.__state or override_cache or not self.enable_cache:
            EdgePiADC.__state = self.__read_registers_to_map()

        # if caching is disabled, don't use cached state for return (dict() deepcopies)
        return (
            EdgePiADC.__state
            if self.enable_cache
            else dict(EdgePiADC.__state)
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
        with self.spi_open():
            out = self.transfer(code)
            _logger.debug(f"__read_register: received {out}")
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
        _logger.debug(f"__write_register: sending {code}")
        with self.spi_open():
            out = self.transfer(code)
        return out

    def __set_rtd_pin(self, enable: bool = False):
        """
        Set or clear RTD_EN pin
        Args:
            enable (bool): RTD enable flag
        Return:
            None
        """
        # pylint: disable=expression-not-assigned
        self.gpio.set_pin_state(RTDPins.RTD_EN.value) if enable else \
        self.gpio.clear_pin_state(RTDPins.RTD_EN.value)

# TODO: To be deleted
    def set_adc_reference(self, reference_config: ADCReferenceSwitching = None):
        """
        Setting ADC referene terminal state. pin 18 and 23 labeled IN GND on the enclosure. It can
        be configured as regular 0V GND or 12V GND.

        Args:
            reference_config: (ADCReferenceSwitching): selecting none, 1, 2, both
        """
        if reference_config == ADCReferenceSwitching.GND_SW1.value:
            self.gpio.set_pin_state(ADCPins.GNDSW_IN1.value)
            self.gpio.clear_pin_state(ADCPins.GNDSW_IN2.value)
        elif reference_config == ADCReferenceSwitching.GND_SW2.value:
            self.gpio.set_pin_state(ADCPins.GNDSW_IN2.value)
            self.gpio.clear_pin_state(ADCPins.GNDSW_IN1.value)
        elif reference_config == ADCReferenceSwitching.GND_SW_BOTH.value:
            self.gpio.set_pin_state(ADCPins.GNDSW_IN1.value)
            self.gpio.set_pin_state(ADCPins.GNDSW_IN2.value)
        elif reference_config == ADCReferenceSwitching.GND_SW_NONE.value:
            self.gpio.clear_pin_state(ADCPins.GNDSW_IN1.value)
            self.gpio.clear_pin_state(ADCPins.GNDSW_IN2.value)

    def stop_conversions(self, adc_num: ADCNum):
        """
        Halt voltage read conversions when ADC is set to perform continuous conversions
        """
        stop_cmd = self.adc_ops.stop_adc(adc_num=adc_num.value)
        with self.spi_open():
            self.transfer(stop_cmd)

    def __send_start_command(self, adc_num: ADCNum):
        """Triggers ADC conversion(s)"""
        start_cmd = self.adc_ops.start_adc(adc_num=adc_num.value)
        with self.spi_open():
            self.transfer(start_cmd)

    def start_conversions(self, adc_num: ADCNum):
        """
        Start ADC voltage read conversions. If ADC is continuous conversion mode,
        this method must be called before performing reads. If ADC is in
        pulse conversion mode, this method does not need to be called before
        performing reads.
        """
        # get state for configs relevant to conversion delay
        state = self.get_state()
        conv_mode = state.adc_1.conversion_mode.code
        data_rate = (
            state.adc_1.data_rate.code if adc_num == ADCNum.ADC_1 else state.adc_2.data_rate.code
        )
        filter_mode = state.filter_mode.code

        conv_delay = expected_initial_time_delay(
            adc_num, data_rate.value.op_code, filter_mode.value.op_code
        )
        _logger.debug(
            (
                f"\nComputed time delay = {conv_delay} (ms) with the following config opcodes:\n"
                f"adc_num={adc_num}, conv_mode={hex(conv_mode.value.op_code)}, "
                f"data_rate={hex(data_rate.value.op_code)}, "
                f"filter_mode={hex(filter_mode.value.op_code)}\n"
            )
        )
        self.__send_start_command(adc_num)
        # apply delay for first conversion
        time.sleep(conv_delay / 1000)

    def clear_reset_bit(self):
        """
        Clear the ADC reset bit. This reset bits acts as a flag that is raised when the ADC
        resets, which automatically happens during power on, or when a reset command is passed.
        Clearing this bit allows subsequent non-standard resets to be detected (by reading the
        STATUS byte of a voltage read).
        """
        self.__config(reset_clear=ADCPower.RESET_CLEAR)

    def __read_data(self, adc: ADCNum, data_size: int):
        """Sends command to ADC to get new voltage conversion data"""
        with self.spi_open():
            return self.transfer([adc.value.read_cmd] + [255] * data_size)

    def __voltage_read(self, adc_num: ADCNum):
        """
        Performs ADC voltage read and formats output into status, voltage,
        and check bytes

        Returns:
            int, list[int], int: uint values of representations of voltage read data ordered as
                (status_byte, voltage_data_bytes, check_byte)
        """
        read_data = self.__read_data(adc_num, ADC_VOLTAGE_READ_LEN)
        if len(read_data) - 1 != ADC_VOLTAGE_READ_LEN:
            raise VoltageReadError(
                f"Voltage read failed: incorrect number of bytes ({len(read_data)}) retrieved"
            )
        status_code = read_data[1]
        voltage_code = read_data[2 : (2 + adc_num.value.num_data_bytes)]
        check_code = read_data[6]
        check_crc(voltage_code, check_code)
        return status_code, voltage_code, check_code

    @staticmethod
    def __get_diff_id(mux_p: PropertyValue, mux_n: PropertyValue) -> int:
        """
        Get differential pair id number for retrieving differential pair calibration values
        """
        #  values are the keys from adc_calib_params
        diff_ids = {
                DiffMode.DIFF_1.value: 8,
                DiffMode.DIFF_2.value: 9,
                DiffMode.DIFF_3.value: 10,
                DiffMode.DIFF_4.value: 11,
            }
        diff_pair = DifferentialPair(mux_p.code, mux_n.code)
        diff_id = diff_ids.get(diff_pair)
        if diff_id is None:
            raise InvalidDifferentialPairError(
                    f"Cannot retrieve calibration values for invalid differential pair {diff_pair}"
                    )
        return diff_id

    def __get_calibration_values(self, adc_calibs: dict, adc_num: ADCNum) -> CalibParam:
        """
        Retrieve voltage reading calibration values based on currently configured
        input multiplexer channels

        Args:
            `adc_calibs` (dict): eeprom adc calibration values
            `adc_num` (ADCNum): adc number voltage is being read from

        Returns:
            `CalibParam`: gain and offset values for voltage reading calibration
        """
        state = self.get_state()
        mux_p = attrgetter(f"adc_{adc_num.value.id_num}.mux_p")(state)
        mux_n = attrgetter(f"adc_{adc_num.value.id_num}.mux_n")(state)

        # assert neither mux is set to float mode
        if CH.FLOAT in (mux_p.code, mux_n.code):
            raise ValueError("Cannot retrieve calibration values for channel in float mode")

        calib_key = mux_p.value if mux_n.code == CH.AINCOM else self.__get_diff_id(mux_p, mux_n)
        calibs = adc_calibs[calib_key]

        if calibs is None:
            _logger.error("Failed to find ADC calibration values")
            raise CalibKeyMissingError(
                (
                    "Failed to retrieve calibration values from eeprom dictionary: "
                    f"dict is missing key = {calib_key}"
                    f"\neeprom_calibs = \n{adc_calibs}"
                )
            )

        return calibs

    def __continuous_time_delay(self, adc_num: ADCNum, state: ADCState):
        """Compute and enforce continuous conversion time delay"""
        # get continuous mode time delay and wait here (delay is needed between each conversion)
        data_rate = (
            state.adc_1.data_rate.code if adc_num == ADCNum.ADC_1 else state.adc_2.data_rate.code
        )
        delay = expected_continuous_time_delay(adc_num, data_rate.value.op_code)

        time.sleep(delay / 1000)

    def __check_adc_1_conv_mode(self, state: ADCState):
        # assert adc is in continuous mode
        if state.adc_1.conversion_mode.code != ConvMode.CONTINUOUS:
            raise ContinuousModeError(
                "ADC1 must be in CONTINUOUS conversion mode in order to call this method."
            )

    def read_voltage(self, adc_num: ADCNum):
        """
        Read voltage input to either ADC1 or ADC2, when performing single channel reading
        or differential reading. For ADC1 reading, only use this method when ADC1 is configured
        to `CONTINUOUS` conversion mode. For `PULSE` conversion mode, use `single_sample` instead.

        Args:
            `adc_num` (ADCNum): the ADC to be read

        Returns:
            `float`: input voltage (V) read from the indicated ADC
        """
        single_ended = False
        state = self.get_state()
        if adc_num == ADCNum.ADC_1:
            self.__check_adc_1_conv_mode(state)
            # Check whether the ADC is either in single-ended or differential
            if state.adc_1.mux_n.code == CH.AINCOM:
                single_ended = True
        else:
            if state.adc_2.mux_n.code == CH.AINCOM:
                single_ended = True

        self.__continuous_time_delay(adc_num, state)

        status_code, voltage_code, _ = self.__voltage_read(adc_num)

        # log STATUS byte
        status = get_adc_status(status_code)
        _logger.debug(f" read_voltage: Logging STATUS byte:\n{status}")

        calibs = self.__get_calibration_values(self.adc_calib_params[adc_num], adc_num)
        _logger.debug(f" read_voltage: gain {calibs.gain}, offset {calibs.offset}")
        # convert from code to voltage

        return code_to_voltage_single_ended(voltage_code, adc_num.value, calibs) if single_ended\
            else code_to_voltage(voltage_code, adc_num.value, calibs)


    def read_rtd_temperature(self):
        """
        Read RTD temperature continuously. Note, to obtain valid temperature values,
        RTD mode must first be enabled by calling `rtd_mode`. ADC1 must also be configured
        to `CONTINUOUS` conversion mode via `set_config`, before calling this method.

        Returns:
            `float`: RTD measured temperature (°C)
        """
        state = self.get_state()
        adc_num = state.rtd_adc
        if adc_num == ADCNum.ADC_1:
            self.__check_adc_1_conv_mode(state)
        self.__continuous_time_delay(adc_num, state)

        _, voltage_code, _ = self.__voltage_read(adc_num)

        return code_to_temperature(
            voltage_code,
            self.rtd_calib.rtd_resistor,
            self.rtd_sensor_resistance,
            self.rtd_sensor_resistance_variation,
            self.rtd_calib.rtd.gain,
            self.rtd_calib.rtd.offset,
            adc_num
        )

    def __enforce_pulse_mode(self, state: ADCState):
        # assert adc is in PULSE mode (check ADCState) -> set to PULSE if not
        if state.adc_1.conversion_mode.code != ConvMode.PULSE:
            self.__config(conversion_mode=ConvMode.PULSE)

    def single_sample(self):
        """
        Trigger a single ADC1 voltage sampling event, when performing single channel reading or
        differential reading. ADC1 must be in `PULSE` conversion mode before calling this method.
        Do not call this method for voltage reading if ADC is configured to `CONTINUOUS`
        conversion mode: use `read_voltage` instead.

        Returns:
            `float`: input voltage (V) read from ADC1
        """
        state = self.get_state()
        single_ended = False
        # Check whether the ADC is either in single-ended or differential
        if state.adc_1.mux_n.code == CH.AINCOM:
            single_ended = True

        self.__enforce_pulse_mode(state)

        # send command to trigger conversion
        self.start_conversions(ADCNum.ADC_1)

        # send command to read conversion data.
        status_code, voltage_code, _ = self.__voltage_read(ADCNum.ADC_1)

        # log STATUS byte
        status = get_adc_status(status_code)
        _logger.debug(f"single_sample: Logging STATUS byte:\n{status}")

        calibs = self.__get_calibration_values(self.adc_calib_params[ADCNum.ADC_1], ADCNum.ADC_1)

        # convert from code to voltage
        _logger.debug(f" read_voltage: code {voltage_code}")
        _logger.debug(f" read_voltage: gain {calibs.gain}, offset {calibs.offset}")
        return code_to_voltage_single_ended(voltage_code, ADCNum.ADC_1.value, calibs) if \
            single_ended  else code_to_voltage(voltage_code, ADCNum.ADC_1.value, calibs)

    def single_sample_rtd(self):
        """
        Trigger a single RTD temperature sampling event. Note, to obtain valid temperature values,
        RTD mode must first be enabled by calling `rtd_mode`. ADC1 must also be configured
        to `PULSE` conversion mode via `set_config`, before calling this method.

        Returns:
            `float`: RTD measured temperature (°C)
        """
        state = self.get_state()
        adc_num = state.rtd_adc
        if adc_num == ADCNum.ADC_1:
            self.__enforce_pulse_mode(state)

        # send command to trigger conversion
        self.start_conversions(adc_num)

        # send command to read conversion data.
        _, voltage_code, _ = self.__voltage_read(adc_num)

        return code_to_temperature(
            voltage_code,
            self.rtd_calib.rtd_resistor,
            self.rtd_sensor_resistance,
            self.rtd_sensor_resistance_variation,
            self.rtd_calib.rtd.gain,
            self.rtd_calib.rtd.offset,
            adc_num
        )

    def reset(self):
        """
        Reset ADC register values to EdgePi ADC power-on state.
        Note this state differs from ADS1263 default power-on, due to
        application of custom power-on configurations required by EdgePi.
        """
        with self.spi_open():
            self.transfer(self.adc_ops.reset_adc())
        self.__reapply_config()

    def __is_data_ready(self, adc_num: ADCNum):
        # pylint: disable=unused-private-member
        # required for integration testing in test_conversion_times.py
        """Utility for testing conversion times, returns True if ADC indicates new voltage data"""
        with self.spi_open():
            read_data = self.transfer([adc_num.value.read_cmd] + [255] * 6)
            if adc_num is ADCNum.ADC_1:
                ready = (read_data[1] & 0b01000000) == 0b01000000
            if adc_num is ADCNum.ADC_2:
                ready = (read_data[1] & 0b10000000) == 0b10000000
            return ready

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
        # _logger.debug(f"__read_registers_to_map: {reg_dict}")

        return reg_dict

    def __is_rtd_on(self):
        """
        Check whether the RTD is enabled or disabled
        Args:
            N/A
        Return:
            rtd_pin_state (bool): True RTD enabled, False RTD disabled
        """
        pin_state = self.gpio.read_pin_state(RTDPins.RTD_EN.value)
        pin_dir = self.gpio.get_pin_direction(RTDPins.RTD_EN.value)
        if pin_state and not pin_dir:
            return True
        return False

    def __get_rtd_state(self):
        """
        Get RTD state this includes the corrent mode (on/off) and the adc type being used
        (adc1 or adc2).
        Returns:
            rtd_mode (dictionary): RTD mode dictionary {"name of config": op_codes}
            rtd_adc (ADCNum): None, no adc attached to RTD, ADCNum.ADC1 or ADCNum.ADC1
        """
        state = self.get_state()
        return state.rtd_mode, state.rtd_adc

    # by default set mux_n's to AINCOM. For diff_mode and rtd_mode, pass in custom mapping.
    # Case 1: user sets to adc_x read ch_x -> mux_n auto mapped to AINCOM
    # Case 2: user sets RTD mode on or off -> mux_n passed in as arg
    # Case 3: user sets any differential mode -> mux_n pass in as arg
    def __get_channel_assign_opcodes(
        self,
        adc_1_mux_p: CH = None,
        adc_2_mux_p: CH = None,
        adc_1_mux_n: CH = CH.AINCOM,
        adc_2_mux_n: CH = CH.AINCOM,
        override_rtd_validation: bool = False
    ):
        """
        Generates OpCodes for assigning positive and negative multiplexers
        of either ADC1 or ADC2 to an ADC input channel. This is needed to allow
        users to assign multiplexers to both ADCs using the same input channel
        number enums.

        Args:
            adc_1_mux_p: input channel to assign to MUXP of ADC1
            adc_2_mux_p: input channel to assign to MUXP of ADC2
            adc_1_mux_n: input channel to assign to MUXN of ADC1
            adc_2_mux_n: input channel to assign to MUXN of ADC2

        Returns:
            `list`: if not empty, contains OpCode(s) for updating multiplexer
                channel assignment for ADC1, ADC2, or both.
        """
        # only update mux_n if mux_p is updated
        if adc_1_mux_p is None:
            adc_1_mux_n = None

        if adc_2_mux_p is None:
            adc_2_mux_n = None

        # no multiplexer config to update
        args = filter_dict_list_key_val(locals(), ["self", "override_rtd_validation"], [None])
        if not args:
            return []

        # allowed channels depend on RTD_EN status
        if not override_rtd_validation:
            channels = list(args.values())
            rtd_enabled = self.__is_rtd_on()
            validate_channels_allowed(channels, rtd_enabled)

        adc_mux_updates = {
            ADCReg.REG_INPMUX: (adc_1_mux_p, adc_1_mux_n),
            ADCReg.REG_ADC2MUX: (adc_2_mux_p, adc_2_mux_n),
        }

        opcodes = generate_mux_opcodes(adc_mux_updates)

        return opcodes

    def select_differential(self, adc: ADCNum, diff_mode: DiffMode):
        """
        Select a differential voltage sampling mode for either ADC1 or ADC2

        Args:
            `adc` (ADCNum): identity of ADC to configure

            `diff_mode` (DiffMode): a pair of input channels to sample, or off

        Raises:
            `KeyError`: if adc is not a valid ADCNum enum
        """
        mux_p = diff_mode.value.mux_p
        mux_n = diff_mode.value.mux_n
        mux_properties = {
            ADCNum.ADC_1: {
                "adc_1_ch": mux_p,
                "adc_1_mux_n": mux_n,
            },
            ADCNum.ADC_2: {
                "adc_2_ch": mux_p,
                "adc_2_mux_n": mux_n,
            },
        }
        diff_update = mux_properties[adc]
        self.__config(**diff_update)

    def  __validate_no_rtd_conflict(self, updates: dict):
        """
        Checks no RTD related properties are being updated if RTD mode is enabled

        Args:
            `updates` (dict): updates formatted as {'property_name': update_value}

        Raises:
            `RTDEnabledError`: if RTD is enabled and an RTD related property is in updates
        """
        rtd_mode, rtd_adc = self.__get_rtd_state()
        if rtd_mode is None or rtd_mode == RTDModes.RTD_OFF:
            return None

        # rtd_properties RTDModes.RTD1_ON or RTDModes.RTD2_ON
        rtd_properties = rtd_mode.value | (ADC1RtdConfig.ON.value if rtd_adc == ADCNum.ADC_1 else\
                                           ADC2RtdConfig.ON.value)
        for update in updates:
            if update in rtd_properties:
                raise RTDEnabledError(
                    f"ADC property '{update}' cannot be updated while RTD is enabled"
                )
        return None

    def __check_adc_pins(self):
        """
        check pin mux of each adc
        Args:
            N/A
        Return:
            channels
        """
        state = self.get_state()
        adc_1_muxs = [state.adc_1.mux_n.code.value, state.adc_1.mux_p.code.value]
        adc_2_muxs = [state.adc_2.mux_n.code.value, state.adc_2.mux_p.code.value]
        return adc_1_muxs, adc_2_muxs

    def __get_rtd_on_update_config(self, muxs: list, adc_num: ADCNum):
        """
        generate a dictionary of config parameters to enable RTD using specified ADC
        Args:
            muxs (list): list of input multiplexer of other ADC [negative input, positive input]
            adc_num (ADCNum): ADC to read RTD
        Return:
            updates (dictionary): configuration dictionary for enabling RTD
                                    {name_of_config : op_codes}
        """
        if any(mux not in [x.value for x in AllowedChannels.RTD_ON.value] for mux in muxs):
            updates = RTDModes.RTD_ON.value |\
            (ADC2RtdConfig.OFF.value if adc_num == ADCNum.ADC_1 else ADC1RtdConfig.OFF.value) |\
            (ADC1RtdConfig.ON.value if adc_num ==ADCNum.ADC_1 else ADC2RtdConfig.ON.value)
        else:
            updates = RTDModes.RTD_ON.value |\
            (ADC1RtdConfig.ON.value if adc_num ==ADCNum.ADC_1 else ADC2RtdConfig.ON.value)
        return updates


    def __get_rtd_off_update_config(self, adc_num: ADCNum):
        """
        generate update config dictionary to send to the config method
        Args:
            adc_num (ADCNum): ADC number
        Return:
            updates (dictionary): configuration dictionary for disabling RTD
        """
        updates = RTDModes.RTD_OFF.value |\
        (ADC1RtdConfig.OFF.value if adc_num == ADCNum.ADC_1  else ADC2RtdConfig.OFF.value)
        return updates

    def set_rtd(self, set_rtd: bool, adc_num: ADCNum = ADCNum.ADC_2):
        """
        Enable/Disable RTD with ADC type passed as arguments.

        NOTE: This function enforces only one ADC to be attached to RTD circuit

        Args:
            `set_rtd` (bool): True to enable RTD, False to disable
        """
        if set_rtd:
            # check inputs of both ADCs. Input 5~8 are only available for RTD reading
            mux_1, mux_2 = self.__check_adc_pins()
            # If inputs on another ADC are one of RTD only inputs, reconfigure the pins them to the
            # default setting. And get RTD_ON configuration values
            updates = self.__get_rtd_on_update_config(
                           mux_2 if adc_num == ADCNum.ADC_1 else mux_1, adc_num)
            # enable RTD pin to re-route internal circuit
            self.__set_rtd_pin(set_rtd)
        else:
            updates = self.__get_rtd_off_update_config(adc_num)
            self.__set_rtd_pin(set_rtd)

        self.__config(**updates, override_rtd_validation=True)

    @staticmethod
    def __extract_mux_args(args: dict) -> dict:
        """
        Checks args dictionary for input multiplexer settings

        Args:
            `args` (dict): args formatted as {'arg_name': value}

        Returns:
            `dict`: input multiplexer args formatted as {'mux_name': value}
        """
        mux_arg_names = {
            "adc_1_ch": "adc_1_mux_p",
            "adc_2_ch": "adc_2_mux_p",
            "adc_1_mux_n": "adc_1_mux_n",
            "adc_2_mux_n": "adc_2_mux_n",
        }
        only_mux_args = {}
        for arg, mux_name in mux_arg_names.items():
            if args.get(arg) is not None:
                only_mux_args[mux_name] = args[arg]
        return only_mux_args

    def __config(
        self,
        adc_1_ch: CH = None,
        adc_2_ch: CH = None,
        adc_1_mux_n: CH = None,
        adc_2_mux_n: CH = None,
        adc_1_data_rate: ADC1DataRate = None,
        adc_2_data_rate: ADC2DataRate = None,
        adc_1_pga: ADC1PGA = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
        checksum_mode: CheckMode = None,
        reset_clear: ADCPower = None,
        idac_1_mux: IDACMUX = None,
        idac_2_mux: IDACMUX = None,
        idac_1_mag: IDACMAG = None,
        idac_2_mag: IDACMAG = None,
        pos_ref_inp: REFMUX = None,
        neg_ref_inp: REFMUX = None,
        adc2_ref_inp: ADC2REFMUX = None,
        override_updates_validation: bool = False,
        override_rtd_validation: bool = False,
    ):
        """
        Configure all ADC settings, either collectively or individually.
        Warning: for internal EdgePi developer use only, users should use
        `set_config()` for modifying settings instead.

        Args:
            `adc_1_ch` (ADCChannel): input voltage channel to map to ADC1 mux_p
            `adc_2_ch` (ADCChannel): input voltage channel to map to ADC2 mux_p
            `adc_1_mux_n` (ADCChannel): input voltage channel to map to ADC1 mux_n
            `adc_2_mux_n` (ADCChannel): input voltage channel to map to ADC1 mux_n
            `adc_1_data_rate` (ADC1DataRate): ADC1 data rate in samples per second
            `adc_2_data_rate` (ADC2DataRate): ADC2 data rate in samples per second,
            `adc_1_pga` (ADC1PGA): enable or bypass PGA,
            `filter_mode` (FilterMode): filter mode for both ADC1 and ADC2.
                Note this affects data rate. Please refer to module documentation
                for more information.
            `conversion_mode` (ConvMode): set conversion mode for ADC1.
                Note, ADC2 runs only in continuous conversion mode.
            `checksum_mode` (CheckMode): set mode for CHECK byte
            `reset_clear` (ADCPower): set state of ADC RESET bit
            `idac_1_mux` (IDACMUX): set analog input pin to connect IDAC1
            `idac_2_mux` (IDACMUX): set analog input pin to connect IDAC2
            `idac_1_mag` (IDACMAG): set the current value for IDAC1
            `idac_2_mag` (IDACMAG): set the current value for IDAC2
            `pos_ref_inp` (REFMUX): set the positive reference input
            `neg_ref_inp` (REFMUX): set the negative reference input
            `override_updates_validation` (bool): set to True to override post-update validation
            `override_rtd_validation` (bool): turn off RTD property validation for RTD mode updates
        """
        # pylint: disable=unused-argument
        # filter out self and None args
        args = filter_dict(locals(), "self", None)
        _logger.debug(f"__config: args after filtering out None defaults:\n{args}")

        # permit updates by rtd_mode() to turn RTD off when it's on, validate other updates
        if not override_rtd_validation:
            self.__validate_no_rtd_conflict(args)

        # get opcodes for mapping multiplexers
        mux_args = self.__extract_mux_args(args)
        ops_list = self.__get_channel_assign_opcodes(
            **mux_args, override_rtd_validation=override_rtd_validation
        )

        # extract OpCode type args, since args may contain non-OpCode args
        args = list(args.values())
        ops_list += [
            entry.value
            for entry in args
            if issubclass(entry.__class__, Enum) and isinstance(entry.value, OpCode)
        ]

        # get current register values
        reg_values = self.__get_register_map()
        _logger.debug(f"__config: register values before updates:\n{reg_values}")

        # get codes to update register values
        updated_reg_values = apply_opcodes(dict(reg_values), ops_list)
        _logger.debug(f"__config: register values after updates:\n{reg_values}")

        # write updated reg values to ADC using a single write.
        data = [entry["value"] for entry in updated_reg_values.values()]
        self.__write_register(ADCReg.REG_ID, data)

        # update ADC state (for state caching)
        self.__update_cache_map(updated_reg_values)

        # validate updates were applied correctly
        if not override_updates_validation:
            self.__validate_updates(updated_reg_values)

        return updated_reg_values

    def __validate_updates(self, updated_reg_values: dict):
        """
        Validates updated config values have been applied to ADC registers.

        Args:
            updated_reg_values (dict): register values that were applied in latest __config()
        """
        reg_values = self.__get_register_map()

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
        adc_1_analog_in: AnalogIn = None,
        adc_1_data_rate: ADC1DataRate = None,
        adc_2_analog_in: AnalogIn = None,
        adc_2_data_rate: ADC2DataRate = None,
        filter_mode: FilterMode = None,
        conversion_mode: ConvMode = None,
        override_updates_validation: bool = False,
        adc_1_pga: ADC1PGA = None
    ):
        """
        Configure user accessible ADC settings, either collectively or individually.

        Args:
            `adc_1_analog_in` (AnalogIn): the input voltage channel to measure via ADC1
            `adc_1_data_rate` (ADC1DataRate): ADC1 data rate in samples per second
            `adc_2_analog_in` (AnalogIn): the input voltage channel to measure via ADC2
            `adc_2_data_rate` (ADC2DataRate): ADC2 data rate in samples per second
            `filter_mode` (FilterMode): filter mode for ADC1.
                Note this affects data rate. Please refer to module documentation
                for more information.
            `conversion_mode` (ConvMode): set conversion mode for ADC1.
            `override_updates_validation` (bool): set to True to skip update validation
            `adc_1_pga` (ADC1PGA): enable or bypass PGA
        """
        # pylint: disable=possibly-unused-variable
        # pylint: disable=unused-argument
        adc_1_ch  = self.__analog_in_to_adc_in_map.get(adc_1_analog_in)
        adc_2_ch  = self.__analog_in_to_adc_in_map.get(adc_2_analog_in)

        if adc_1_ch is None and adc_1_analog_in is not None:
            raise TypeError(f"set_config: wrong type passed for adc_1_analog_in: {adc_1_analog_in}")
        if adc_2_ch is None and adc_2_analog_in is not None:
            raise TypeError(f"set_config: wrong type passed for adc_2_analog_in: {adc_2_analog_in}")

        args = filter_dict_list_key_val(locals(),
                                        ["self", "adc_1_analog_in", "adc_2_analog_in"],
                                        [None])
        self.__config(**args)

    def get_state(self, override_cache: bool = False) -> ADCState:
        """
        Read the current hardware state of configurable ADC properties

        Args:
            `override_cache` (bool): force SPI read to get hardware state

        Returns:
            ADCState: information about the current ADC hardware state
        """
        reg_values = self.__get_register_map(override_cache)
        return ADCState(reg_values)
