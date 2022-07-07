"""unit tests for tc_commands.py module"""

import pytest
from bitstring import BitArray
from edgepi.tc.tc_commands import code_to_temp, _negative_temp_check


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
    with pytest.raises(Exception) as e:
        code_to_temp(code_bytes)
    assert e.type == err_type


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
