import pytest
from edgepi.reg_helper.reg_helper import _apply_opcode
from edgepi.tc.tc_constants import *

@pytest.mark.parametrize('reg_value, opcode, updated_reg_value', [
    (0b00000000, ConvMode.AUTO.value, 0b10000000),          # sets bit 7, doesn't set others
    (0b10000000, ConvMode.AUTO.value, 0b10000000),          # doesn't clear bit 7
    (0b01111111, ConvMode.AUTO.value, 0b11111111),          # sets bit 7, doesn't clear others
    (0b11111111, ConvMode.AUTO.value, 0b11111111),          # doesn't clear bit 7 or others
    (0b00000000, ConvMode.SINGLE.value, 0b00000000),        # doesn't set bit 7 or others
    (0b10000000, ConvMode.SINGLE.value, 0b00000000),        # clears bit 7
    (0b11111111, ConvMode.SINGLE.value, 0b01111111),        # clears only bit 7
    (0b00000000, TCOps.SINGLE_SHOT.value, 0b01000000),      # only sets bit 6
    (0b01000000, TCOps.SINGLE_SHOT.value, 0b01000000),      # doesn't clear bit 6
    (0b10111111, TCOps.SINGLE_SHOT.value, 0b11111111),      # sets bit 6, doesn't clear others
    (0b00001000, CJMode.ENABLE.value, 0b00000000),          # clears bit 3
    (0b00000000, CJMode.ENABLE.value, 0b00000000),          # doesn't set bit 3 or others
    (0b00000000, CJMode.DISABLE.value, 0b00001000),         # sets bit 3
    (0b00001000, CJMode.DISABLE.value, 0b00001000),         # doesn't toggle bit 3
    (0b11111111, CJMode.DISABLE.value, 0b11111111),         # doesn't clear others
    (0b00000100, FaultMode.COMPARATOR.value, 0b00000000),   # clears bit 2, doesn't set others
    (0b00000000, FaultMode.COMPARATOR.value, 0b00000000),   # doesn't toggle bit 2
    (0b00000000, FaultMode.INTERRUPT.value, 0b00000100),    # sets bit 2, doesn't set others
    (0b00000100, FaultMode.INTERRUPT.value, 0b00000100),    # doesn't toggle bit 2
    (0b00000000, TCOps.CLEAR_FAULTS.value, 0b00000010),     # sets bit 1, doesn't clear others
    (0b00000001, NoiseFilterMode.Hz_60.value, 0b00000000),  # clear bit 0, doesn't set others
    (0b00000000, NoiseFilterMode.Hz_60.value, 0b00000000),  # doesn't toggle bit 0
    (0b00000000, NoiseFilterMode.Hz_50.value, 0b00000001),  # sets bit 0, doesn't set others
    (0b00000001, NoiseFilterMode.Hz_50.value, 0b00000001),  # doesn't toggle bit 0
    (0b11110000, AvgMode.AVG_1.value, 0b00000000),          # clears high byte, doesn't set low byte
    (0b11100000, AvgMode.AVG_2.value, 0b00010000),          # sets high byte, doesn't set low byte
    (0b11010000, AvgMode.AVG_4.value, 0b00100000),          # sets high byte, doesn't set low byte     
    (0b11000000, AvgMode.AVG_8.value, 0b00110000),          # sets high byte, doesn't set low byte
    (0b10110000, AvgMode.AVG_16.value, 0b01000000),         # sets high byte, doesn't set low byte
    (0b00001111, TCType.TYPE_B.value, 0b00000000),          # sets low byte, doesn't set high byte
    (0b00001110, TCType.TYPE_E.value, 0b00000001),          # sets low byte, doesn't set high byte
    (0b00001101, TCType.TYPE_J.value, 0b00000010),          # sets low byte, doesn't set high byte
    (0b00001100, TCType.TYPE_K.value, 0b00000011),          # sets low byte, doesn't set high byte
    (0b00001011, TCType.TYPE_N.value, 0b00000100),          # sets low byte, doesn't set high byte
    (0b00001010, TCType.TYPE_R.value, 0b00000101),          # sets low byte, doesn't set high byte
    (0b00001001, TCType.TYPE_S.value, 0b00000110),          # sets low byte, doesn't set high byte
    (0b00001000, TCType.TYPE_T.value, 0b00000111),          # sets low byte, doesn't set high byte
    (0b00000111, VoltageMode.GAIN_8.value, 0b00001000),     # sets low byte, doesn't set high byte
    (0b00000011, VoltageMode.GAIN_32.value, 0b00001100),    # sets low byte, doesn't set high byte
])
def test_apply_opcode(reg_value, opcode, updated_reg_value):
    assert _apply_opcode(reg_value, opcode) == updated_reg_value
