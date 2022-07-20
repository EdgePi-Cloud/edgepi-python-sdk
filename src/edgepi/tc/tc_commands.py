"""'
    Accessory module for EdgePiTC methods

    Classes:


    Functions:
        _negative_temp_check(int)
        code_to_temp(list)
"""


import logging
from enum import Enum, unique
from dataclasses import dataclass
from bitstring import BitArray, pack
from edgepi.tc.tc_constants import REG_SIZE, TCAddresses, TCType, TempBits, Masks
from edgepi.reg_helper.reg_helper import OpCode

_logger = logging.getLogger(__name__)


def _negative_temp_check(temp_code: int):
    """checks if MAX31856 temperature register reading is negative"""
    # if sign bit is set (negative temp), toggle sign bit off. Compute as
    # positive and then invert after.
    if temp_code[0]:
        del temp_code[0]
        return True
    return False


def code_to_temp(code_bytes: list):
    """
    converts cold junction and linearized thermocouple temperature
    binary codes to float values
    """
    # generate cold junction temperature and linearized TC temperatures
    cj_high_byte = code_bytes[1]
    cj_low_byte = code_bytes[2]
    lt_high_byte = code_bytes[3]
    lt_mid_byte = code_bytes[4]
    lt_low_byte = code_bytes[5]

    cj_negative_flag, lt_negative_flag = False, False

    # combine and arrange the temperature bits in order from msb to lsb and
    # eliminate empty placeholder bits
    cj_code = pack("uint:8, uint:8", cj_high_byte, cj_low_byte)
    del cj_code[-2:]
    cj_negative_flag = _negative_temp_check(cj_code)

    # combine and arrange the temperature bits in order from msb to lsb and
    # eliminate empty placeholder bits
    lt_code = pack("uint:8, uint:8, uint:8", lt_high_byte, lt_mid_byte, lt_low_byte)
    del lt_code[-5:]
    lt_negative_flag = _negative_temp_check(lt_code)

    # >> shift the 6 precision bits behind the decimal point
    cj_temp = cj_code.uint * (2**-TempBits.CJ_DECIMAL_BITS.value)
    # >> shift the 7 precision bits behind the decimal point
    lt_temp = lt_code.uint * (2**-TempBits.LT_DECIMAL_BITS.value)

    # invert if negative temperature
    if cj_negative_flag:
        cj_temp = -(cj_temp)
    if lt_negative_flag:
        lt_temp = -(lt_temp)

    _logger.info(f"Cold Junction Temp: {cj_temp}")
    _logger.info(f"THERMOCOUPLE TC Temp: {lt_temp}")

    return cj_temp, lt_temp


@unique
class TempType(Enum):
    """MAX31856 temperature threshold setting types"""

    COLD_JUNCTION = 0
    THERMOCOUPLE = 1
    COLD_JUNCTION_OFFSET = 2


@dataclass
class TempCode:
    """Holds data needed to update a MAX31856 temperature threshold configuration, where
    configuring this setting requires updating one or more registers whose bits are
    assigned roles as either sign, integer, decimal, or filler bits.

    Attributes:
        int_val (int): the integer value to be written to this setting

        dec_val (DecBits): the decimal value to be written to this setting, represented
                        as a binary value (uint)

        num_int_bits (int): the number of bits assigned to integer values for this setting

        num_dec_bits (int): the number of bits assigned to decimal values for this setting

        num_int_bits (int): the number of bits assigned to filler values for this setting

        start_addx (int): address of the MSB for this setting

        setting_name (TempType): the name for this temperature setting
    """

    int_val: int
    dec_val: int
    num_int_bits: int
    num_dec_bits: int
    num_filler_bits: int
    start_addx: int
    setting_name: TempType


@dataclass
class TempRange:
    """
    Thermocouple temperature range of allowed values by thermocouple type.

    Attributes:

        tc_low (int): hot-junction lowest temperature

        tc_high (int): hot-junction highest temperature

        cold_junct_low (int): cold-junction lowest temperature

        cold_junct_high (int): cold-junction highest temperature

    """

    tc_low: int
    tc_high: int
    cold_junct_low: int
    cold_junct_high: int


_tc_type_temps = {
    TCType.TYPE_B.value.op_code: TempRange(250, 1820, 0, 125),
    TCType.TYPE_E.value.op_code: TempRange(-200, 1000, -55, 125),
    TCType.TYPE_J.value.op_code: TempRange(-210, 1200, -55, 125),
    TCType.TYPE_K.value.op_code: TempRange(-200, 1372, -55, 125),
    TCType.TYPE_N.value.op_code: TempRange(-200, 1300, -55, 125),
    TCType.TYPE_R.value.op_code: TempRange(-50, 1768, -50, 125),
    TCType.TYPE_S.value.op_code: TempRange(-50, 1768, -50, 125),
    TCType.TYPE_T.value.op_code: TempRange(-200, 400, -55, 125),
}


def _format_temp_bitstring(
    sign_bit: int, int_val: int, dec_val: int, num_int_bits: int, num_dec_bits: int, fill_bits: int
):
    """Combine and place in order the sign, int, dec, and filler bits of a TempCode into a BitArray

    Returns:
        a bitstring BitArray ordered from MSB to LSB as a MAX31856 temperature register: sign_bit,
        int_val, dec_val, fill_bits.
    """
    bits = BitArray(uint=sign_bit, length=1)

    int_bits = BitArray(uint=int_val, length=num_int_bits)
    bits.append(int_bits)
    dec_bits = BitArray(uint=dec_val, length=num_dec_bits) if num_dec_bits else ""
    bits.append(dec_bits)

    # pylint: disable=unused-variable
    for i in range(fill_bits):
        bits += "0b0"
    return bits


def _slice_bitstring_to_opcodes(temp_code: TempCode, bitstr: BitArray, num_slices: int) -> list:
    """Uses a bitstring representing a temperature setting update to produce OpCodes
    for carrying out this operation

    Returns:
        a list of OpCodes
    """
    op_codes = []
    for i in range(num_slices):
        start = i * 8
        end = start + 8
        value = bitstr[start:end].uint
        # create new OpCode, incrementing address to next register each time if
        # this temp_code requires > 1 register.
        op_codes.append(OpCode(value, temp_code.start_addx + i, Masks.BYTE_MASK.value))
    return op_codes


class TempOutOfRangeError(ValueError):
    """Raised when a temperature threshold entered by the user is out of range for the currently
    configured thermocouple type.
    """


class IncompleteTempError(ValueError):
    """Raised when the user sets only either the integer or decimal value
    for a temperature threshold which requires both.
    """


class MissingTCTypeError(ValueError):
    """Raised if no thermocouple type is passed to tempcode_to_opcode"""


class IncompatibleRegisterSizeError(ValueError):
    """Raised when the number of bits contained in a TempCode is not a multiple
    of MAX31856 register sizes (8 bits).
    """


class IllegalTempTypeError(ValueError):
    """Raised when a non-existent TempType is entered"""


class ColdJunctionOverWriteError(Exception):
    """
    Raised when the user attempts to write temperature values to the cold-junction
    sensor without first having disabled it."""


def _dec_bits_to_float(dec_bits: int, num_dec_bits: int, is_negative: bool = False):
    """converts a decimal value formatted as DecBits4 or DecBits6 into float

    Args:
        dec_bits (int): the uint value representing the binary code for decimal value,
                        obtained from a DecBits4 or DecBits6 enum.

        num_dec_bits (int): the number of bits assigned for decimal values

        is_negative (bool): is this a negative decimal value or not
    """
    # shift the bits num_dec_bits places behind the decimal point
    if num_dec_bits == 0:
        return 0

    return (dec_bits * 2**-num_dec_bits) * (-1 if is_negative else 1)


def _validate_temperatures(tempcode: TempCode, tc_type: TCType):
    """Validates that the integer value of a TempCode is within the permitted range for
    the targeted register or thermocouple type.
    """
    # use thermocouple type to get TempRange object from dict
    temps = _tc_type_temps[tc_type.value.op_code]

    temp_ranges = {
        TempType.COLD_JUNCTION.value: {"min": temps.cold_junct_low, "max": temps.cold_junct_high},
        TempType.THERMOCOUPLE.value: {"min": temps.tc_low, "max": temps.tc_high},
        TempType.COLD_JUNCTION_OFFSET.value: {"min": -7, "max": 7},
    }
    is_negative = bool(tempcode.int_val < 0)
    temp_type = tempcode.setting_name.value
    temp_val = tempcode.int_val + _dec_bits_to_float(
        tempcode.dec_val.value, tempcode.num_dec_bits, is_negative
    )

    if temp_type not in temp_ranges:
        raise IllegalTempTypeError(f"TempType {temp_type} does not exist")

    if not temp_ranges[temp_type]["min"] <= temp_val <= temp_ranges[temp_type]["max"]:
        raise TempOutOfRangeError(
            f"""Temperature integer value {temp_val} exceeds writeable limits
        for setting {tempcode.setting_name} for {tc_type} thermocouple"""
        )


def tempcode_to_opcode(temp_code: TempCode, tc_type: TCType, cj_status: bool) -> list:
    """
    Generates a list of OpCodes necessary to execture the temperature setting
    updates contained in a TempCode.

    Returns:
        A list of OpCode objects

    Raises:
        ValueError: if temp_code is None

        IncompleteTempError: if TempCode object only has either an integer or decimal value

        MissingTCTypeError: if thermocouple type is not provided

        IncompatibleRegisterSizeError: if number of bits in TempCode object is not divisible by
                                        MAX31856 register size of 8 bits.

        ColdJunctionOverWriteError: if value is written to cold-junction temperature registers
                                    while cold-junction sensing is not disabled.
    """
    # pylint: disable=too-many-branches

    if temp_code is None:
        raise ValueError("temp_code must be of type TempCode: received None")

    # no args passed for this temp setting -- skip it
    # second clause is to check for registers with no decimal bits,
    # since dec_val will never be None
    if temp_code.int_val is None and (temp_code.dec_val is None or temp_code.num_dec_bits == 0):
        return []

    # only either int or dec args passed for this temp setting
    if temp_code.int_val is None or temp_code.dec_val is None:
        raise IncompleteTempError(
            f"temp_code {temp_code} requires both int and dec values: received only one of these."
        )

    if tc_type is None:
        raise MissingTCTypeError(
            "thermocouple type is required to compute thermocouple temperature range"
        )

    if not cj_status and temp_code.start_addx == TCAddresses.CJTH_W.value:
        raise ColdJunctionOverWriteError(
            "Cold-junction sensor must be disabled in order to write temperature values to it"
        )

    # validate temp range
    _validate_temperatures(temp_code, tc_type)

    # compute total bits required by this setting
    num_bits = 1 + temp_code.num_int_bits + temp_code.num_dec_bits + temp_code.num_filler_bits

    if num_bits % REG_SIZE:
        raise IncompatibleRegisterSizeError(
            "Number of temp_code bits not divisible by 8 bit register size"
        )

    # check if negative temperature
    sign_bit = 0
    if temp_code.int_val < 0:
        sign_bit = 1
        temp_code.int_val = abs(temp_code.int_val)

    # combine and place in order the sign, int, dec, and filler bits into a BitArray
    bits = _format_temp_bitstring(
        sign_bit,
        temp_code.int_val,
        temp_code.dec_val.value,
        temp_code.num_int_bits,
        temp_code.num_dec_bits,
        temp_code.num_filler_bits,
    )

    # slice bitstring into 8-bit register sized chunks and convert each chunk to OpCode
    num_regs = int(num_bits / REG_SIZE)  # number of registers this setting uses
    return _slice_bitstring_to_opcodes(temp_code, bits, num_regs)
