import pytest
from edgepi.reg_helper.reg_helper import _apply_opcode
from edgepi.tc.tc_constants import *

@pytest.mark.parametrize('reg_value, opcode, updated_reg_value', [
    (0b00000000, ConvMode.AUTO.value, 0b10000000),
    (0b10000000, ConvMode.AUTO.value, 0b10000000),
    (0b00000000, ConvMode.SINGLE.value, 0b00000000),
    (0b10000000, ConvMode.SINGLE.value, 0b00000000),
])
def test_apply_opcode(reg_value, opcode, updated_reg_value):
    assert _apply_opcode(reg_value, opcode) == updated_reg_value
