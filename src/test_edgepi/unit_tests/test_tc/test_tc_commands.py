"""unit tests for tc_commands.py module"""


from collections import Counter
from contextlib import nullcontext as does_not_raise

import pytest
from bitstring import BitArray
from edgepi.reg_helper.reg_helper import OpCode
from edgepi.tc.tc_constants import DecBits4, DecBits6, Masks, TCAddresses, TCType
from edgepi.tc.tc_commands import (
    ColdJunctionOverWriteError,
    IncompatibleRegisterSizeError,
    IncompleteTempError,
    MissingTCTypeError,
    TempOutOfRangeError,
    TempType,
    _dec_bits_to_float,
    code_to_temp,
    _negative_temp_check,
    tempcode_to_opcode,
    TempCode,
    _validate_temperatures,
)


@pytest.mark.parametrize(
    "code_bytes, temps",
    [
        ([0x0D, 0x88, 0x00, 0xC0, 0x00, 0x00], (-8, -1024)),  # negative temps
        ([0x0D, 0x08, 0x00, 0x40, 0x00, 0x00], (8, 1024)),  # positive temps
        (
            [0x0D, 0x7F, 0xFC, 0x7F, 0xFF, 0xE0],
            (127.984375, 2047.9921875),
        ),  # max temp values
        (
            [0x0D, 0xFF, 0xFC, 0xFF, 0xFF, 0xE0],
            (-127.984375, -2047.9921875),
        ),  # min temp values
        ([0x0D, 0x00, 0x00, 0x00, 0x00, 0x00], (0, 0)),  # zero temp
        ([0x0D, 0x15, 0x00, 0x01, 0x50, 0x00], (21, 21)),  # room temperature values
    ],
)
def test_code_to_temp(code_bytes, temps):
    assert code_to_temp(code_bytes) == temps


@pytest.mark.parametrize(
    "code_bytes, err_type",
    [
        ([0x0D], IndexError),  # should raise IndexError
        (
            [0x0D, "hello", "world", "!", 0x0F, 0x0F],
            ValueError,
        ),  # should raise ValueError
    ],
)
def test_code_to_temp_exceptions(code_bytes, err_type):
    with pytest.raises(Exception) as err:
        code_to_temp(code_bytes)
    assert err.type == err_type


@pytest.mark.parametrize(
    "temp_code, out, new_value",
    [
        (BitArray(uint=0b10001000, length=8), True, 0b1000),
        (BitArray(uint=0b01001000, length=8), False, 0b01001000),
    ],
)
def test_negative_temp_check(temp_code, out, new_value):
    assert _negative_temp_check(temp_code) == out
    assert temp_code.uint == new_value


@pytest.mark.parametrize(
    "tempcode, tc_type, opcode_list",
    [
        (
            TempCode(125, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            [OpCode(0x7D, TCAddresses.CJHF_W.value, Masks.BYTE_MASK.value)],
        ),  # single register, + value, no dec, no fillers
        (
            TempCode(-55, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            [OpCode(0xB7, TCAddresses.CJHF_W.value, Masks.BYTE_MASK.value)],
        ),  # single register, - value, no dec, no fillers
        (
            TempCode(
                0x4, DecBits4.P0_5, 3, 4, 0, TCAddresses.CJTO_W.value, TempType.COLD_JUNCTION_OFFSET
            ),
            TCType.TYPE_K,
            [OpCode(0x48, TCAddresses.CJTO_W.value, Masks.BYTE_MASK.value)],
        ),  # single register, + value, dec, no fillers
        (
            TempCode(
                -0x4,
                DecBits4.P0_5,
                3,
                4,
                0,
                TCAddresses.CJTO_W.value,
                TempType.COLD_JUNCTION_OFFSET,
            ),
            TCType.TYPE_K,
            [OpCode(0xC8, TCAddresses.CJTO_W.value, Masks.BYTE_MASK.value)],
        ),  # single register, - value, dec, no fillers
        (
            TempCode(
                1024, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            [
                OpCode(0x40, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x00, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, - value, no dec, no fillers
        (
            TempCode(-50, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE),
            TCType.TYPE_K,
            [
                OpCode(0x83, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x20, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, - value, no dec, no fillers
        (
            TempCode(
                1024, DecBits4.P0_75, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            [
                OpCode(0x40, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x0C, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, + value, dec, no fillers
        (
            TempCode(
                -50, DecBits4.P0_75, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            [
                OpCode(0x83, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x2C, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, - value, dec, no fillers
        (
            TempCode(
                1371, DecBits4.P0_9375, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            [
                OpCode(0x55, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0xBF, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, max + value, dec, no fillers
        (
            TempCode(
                64, DecBits6.P0_296875, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION
            ),
            TCType.TYPE_K,
            [
                OpCode(0x40, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x4C, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, + value, dec, fillers
        (
            TempCode(
                -8, DecBits6.P0_296875, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION
            ),
            TCType.TYPE_K,
            [
                OpCode(0x88, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x4C, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, - value, dec, fillers
        (
            TempCode(
                124, DecBits6.P0_984375, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION
            ),
            TCType.TYPE_K,
            [
                OpCode(0x7C, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0xFC, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, max + value, dec, fillers
        (
            TempCode(
                1, DecBits6.P0_015625, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION
            ),
            TCType.TYPE_K,
            [
                OpCode(0x01, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x04, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, min + value, dec, fillers
        (
            TempCode(0, DecBits6.P0, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            [
                OpCode(0x00, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x00, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, zero value, dec, fillers
        (
            TempCode(
                -1, DecBits6.P0_015625, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION
            ),
            TCType.TYPE_K,
            [
                OpCode(0x81, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0x04, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, max - value, dec, fillers
        (
            TempCode(
                -25, DecBits6.P0_984375, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION
            ),
            TCType.TYPE_K,
            [
                OpCode(0x99, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
                OpCode(0xFC, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value),
            ],
        ),  # 2 registers, min - value, dec, fillers
        (
            TempCode(None, None, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            [],
        ),
    ],
)
def test_tempcode_to_opcode(tempcode, tc_type, opcode_list):
    result = tempcode_to_opcode(tempcode, tc_type, True)
    assert Counter(result) == Counter(opcode_list)


@pytest.mark.parametrize(
    "tempcode, tc_type, cj_status, err_type",
    [
        (
            TempCode(127, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            True,
            TempOutOfRangeError,
        ),
        (
            TempCode(127, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            True,
            TempOutOfRangeError,
        ),
        (None, TCType.TYPE_K, True, ValueError),
        (
            TempCode(None, DecBits6.P0, 7, 6, 2, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            True,
            IncompleteTempError,
        ),
        (
            TempCode(1000, None, 7, 6, 2, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            True,
            IncompleteTempError,
        ),
        (
            TempCode(120, DecBits4.P0, 8, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            True,
            IncompatibleRegisterSizeError,
        ),
        (
            TempCode(120, DecBits4.P0, 7, 1, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            True,
            IncompatibleRegisterSizeError,
        ),
        (
            TempCode(120, DecBits4.P0, 6, 1, 1, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            True,
            IncompatibleRegisterSizeError,
        ),
        (
            TempCode(127, DecBits4.P0, 8, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            None,
            True,
            MissingTCTypeError,
        ),
        (
            TempCode(120, DecBits4.P0, 6, 1, 1, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            False,
            ColdJunctionOverWriteError,
        ),
    ],
)
def test_tempcode_to_opcode_raises(tempcode, tc_type, cj_status, err_type):
    with pytest.raises(Exception) as err:
        tempcode_to_opcode(tempcode, tc_type, cj_status)
    assert err.type == err_type


@pytest.mark.parametrize(
    "tempcode, tc_type, expected",
    [
        (
            TempCode(126, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(125, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            does_not_raise(),
        ),
        (
            TempCode(-56, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(-55, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_K,
            does_not_raise(),
        ),
        (
            TempCode(
                1373, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(
                1372, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            does_not_raise(),
        ),
        (
            TempCode(
                -201, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(
                -200, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            does_not_raise(),
        ),
        (
            TempCode(126, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_B,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(125, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_B,
            does_not_raise(),
        ),
        (
            TempCode(-1, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_B,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(0, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_B,
            does_not_raise(),
        ),
        (
            TempCode(
                1821, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_B,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(
                1820, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_B,
            does_not_raise(),
        ),
        (
            TempCode(249, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE),
            TCType.TYPE_B,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(250, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE),
            TCType.TYPE_B,
            does_not_raise(),
        ),
        (
            TempCode(126, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_E,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(125, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_E,
            does_not_raise(),
        ),
        (
            TempCode(-56, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_E,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(-55, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
            TCType.TYPE_E,
            does_not_raise(),
        ),
        (
            TempCode(
                1001, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_E,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(
                1000, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_E,
            does_not_raise(),
        ),
        (
            TempCode(
                -201, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_E,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(
                -200, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_E,
            does_not_raise(),
        ),
        (
            TempCode(
                1372, DecBits4.P0_25, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(
                1371, DecBits4.P0_4375, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            does_not_raise(),
        ),
        (
            TempCode(
                -200, DecBits4.P0_25, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(
                -199, DecBits4.P0_125, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_K,
            does_not_raise(),
        ),
        (
            TempCode(
                1820, DecBits4.P0_375, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_B,
            pytest.raises(TempOutOfRangeError),
        ),
        (
            TempCode(
                1819, DecBits4.P0_125, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE
            ),
            TCType.TYPE_B,
            does_not_raise(),
        ),
    ],
)
def test_validate_temperatures(tempcode, tc_type, expected):
    with expected:
        _validate_temperatures(tempcode, tc_type)


@pytest.mark.parametrize(
    "dec_bits, num_dec_bits, float_val",
    [
        (DecBits4.P0.value, 4, 0),
        (DecBits4.P0_5.value, 4, 0.5),
        (DecBits4.P0_75.value, 4, 0.75),
        (DecBits4.P0_875.value, 4, 0.875),
        (DecBits4.P0_9375.value, 4, 0.9375),
        (DecBits4.P0_4375.value, 4, 0.4375),
        (DecBits4.P0_1875.value, 4, 0.1875),
        (DecBits4.P0_0625.value, 4, 0.0625),
        (DecBits4.P0_5625.value, 4, 0.5625),
        (DecBits4.P0_8125.value, 4, 0.8125),
        (DecBits4.P0_6875.value, 4, 0.6875),
        (DecBits4.P0_25.value, 4, 0.25),
        (DecBits4.P0_125.value, 4, 0.125),
        (DecBits4.P0_625.value, 4, 0.625),
        (DecBits4.P0_3125.value, 4, 0.3125),
        (DecBits4.P0_375.value, 4, 0.375),
        (DecBits6.P0.value, 6, 0),
        (DecBits6.P0_015625.value, 6, 0.015625),
        (DecBits6.P0_03125.value, 6, 0.03125),
        (DecBits6.P0_046875.value, 6, 0.046875),
        (DecBits6.P0_0625.value, 6, 0.0625),
        (DecBits6.P0_078125.value, 6, 0.078125),
        (DecBits6.P0_09375.value, 6, 0.09375),
        (DecBits6.P0_109375.value, 6, 0.109375),
        (DecBits6.P0_125.value, 6, 0.125),
        (DecBits6.P0_140625.value, 6, 0.140625),
        (DecBits6.P0_15625.value, 6, 0.15625),
        (DecBits6.P0_171875.value, 6, 0.171875),
        (DecBits6.P0_1875.value, 6, 0.1875),
        (DecBits6.P0_203125.value, 6, 0.203125),
        (DecBits6.P0_21875.value, 6, 0.21875),
        (DecBits6.P0_234375.value, 6, 0.234375),
        (DecBits6.P0_25.value, 6, 0.25),
        (DecBits6.P0_265625.value, 6, 0.265625),
        (DecBits6.P0_28125.value, 6, 0.28125),
        (DecBits6.P0_296875.value, 6, 0.296875),
        (DecBits6.P0_3125.value, 6, 0.3125),
        (DecBits6.P0_328125.value, 6, 0.328125),
        (DecBits6.P0_34375.value, 6, 0.34375),
        (DecBits6.P0_359375.value, 6, 0.359375),
        (DecBits6.P0_375.value, 6, 0.375),
        (DecBits6.P0_390625.value, 6, 0.390625),
        (DecBits6.P0_40625.value, 6, 0.40625),
        (DecBits6.P0_421875.value, 6, 0.421875),
        (DecBits6.P0_4375.value, 6, 0.4375),
        (DecBits6.P0_453125.value, 6, 0.453125),
        (DecBits6.P0_46875.value, 6, 0.46875),
        (DecBits6.P0_484375.value, 6, 0.484375),
        (DecBits6.P0_5.value, 6, 0.5),
        (DecBits6.P0_515625.value, 6, 0.515625),
        (DecBits6.P0_53125.value, 6, 0.53125),
        (DecBits6.P0_546875.value, 6, 0.546875),
        (DecBits6.P0_5625.value, 6, 0.5625),
        (DecBits6.P0_578125.value, 6, 0.578125),
        (DecBits6.P0_59375.value, 6, 0.59375),
        (DecBits6.P0_609375.value, 6, 0.609375),
        (DecBits6.P0_625.value, 6, 0.625),
        (DecBits6.P0_640625.value, 6, 0.640625),
        (DecBits6.P0_65625.value, 6, 0.65625),
        (DecBits6.P0_671875.value, 6, 0.671875),
        (DecBits6.P0_6875.value, 6, 0.6875),
        (DecBits6.P0_703125.value, 6, 0.703125),
        (DecBits6.P0_71875.value, 6, 0.71875),
        (DecBits6.P0_734375.value, 6, 0.734375),
        (DecBits6.P0_75.value, 6, 0.75),
        (DecBits6.P0_765625.value, 6, 0.765625),
        (DecBits6.P0_78125.value, 6, 0.78125),
        (DecBits6.P0_796875.value, 6, 0.796875),
        (DecBits6.P0_8125.value, 6, 0.8125),
        (DecBits6.P0_828125.value, 6, 0.828125),
        (DecBits6.P0_84375.value, 6, 0.84375),
        (DecBits6.P0_859375.value, 6, 0.859375),
        (DecBits6.P0_875.value, 6, 0.875),
        (DecBits6.P0_890625.value, 6, 0.890625),
        (DecBits6.P0_90625.value, 6, 0.90625),
        (DecBits6.P0_921875.value, 6, 0.921875),
        (DecBits6.P0_9375.value, 6, 0.9375),
        (DecBits6.P0_953125.value, 6, 0.953125),
        (DecBits6.P0_96875.value, 6, 0.96875),
        (DecBits6.P0_984375.value, 6, 0.984375),
    ],
)
def test_dec_bits_to_float(dec_bits, num_dec_bits, float_val):
    assert _dec_bits_to_float(dec_bits, num_dec_bits) == float_val
