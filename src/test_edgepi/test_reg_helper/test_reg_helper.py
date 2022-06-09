import pytest
from edgepi.reg_helper.reg_helper import _apply_opcode
from edgepi.tc.tc_constants import *

@pytest.mark.parametrize('reg_value, opcode, updated_reg_value', [
    (0b00000000, ConvMode.AUTO.value, 0b10000000),
    (0b10000000, ConvMode.AUTO.value, 0b10000000),
    (0b01111111, ConvMode.AUTO.value, 0b11111111),
    (0b11111111, ConvMode.AUTO.value, 0b11111111),
    (0b00000000, ConvMode.SINGLE.value, 0b00000000),
    (0b10000000, ConvMode.SINGLE.value, 0b00000000),
    (0b10000000, ConvMode.SINGLE.value, 0b00000000),
    (0b11111111, ConvMode.SINGLE.value, 0b01111111),
    (0b00000000, TCOps.SINGLE_SHOT.value, 0b01000000),
    (0b01000000, TCOps.SINGLE_SHOT.value, 0b01000000),
    (0b10111111, TCOps.SINGLE_SHOT.value, 0b11111111),
])
def test_apply_opcode(reg_value, opcode, updated_reg_value):
    assert _apply_opcode(reg_value, opcode) == updated_reg_value
