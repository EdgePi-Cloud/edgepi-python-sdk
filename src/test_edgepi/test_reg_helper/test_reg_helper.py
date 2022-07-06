import pytest
from copy import deepcopy
from edgepi.reg_helper.reg_helper import _apply_opcode, _add_change_flags, apply_opcodes, _convert_values_to_dict
from edgepi.tc.tc_constants import *

@pytest.mark.parametrize('reg_value, opcode, updated_reg_value', [
    (0b00000000, ConvMode.AUTO.value, 0b10000000),          # sets bit 7, doesn't set others
    (0b10000000, ConvMode.AUTO.value, 0b10000000),          # doesn't toggle bit 7
    (0b01111111, ConvMode.AUTO.value, 0b11111111),          # sets bit 7, doesn't clear others
    (0b11111111, ConvMode.SINGLE.value, 0b01111111),        # clears bit 7, doesn't clear others
    (0b00000000, ConvMode.SINGLE.value, 0b00000000),        # doesn't toggle bit 7
    (0b10000000, ConvMode.SINGLE.value, 0b00000000),        # clears bit 7, doesn't set others
    (0b00000000, TCOps.SINGLE_SHOT.value, 0b01000000),      # sets bit 6, doesn't set others
    (0b01000000, TCOps.SINGLE_SHOT.value, 0b01000000),      # doesn't toggle bit 6
    (0b10111111, TCOps.SINGLE_SHOT.value, 0b11111111),      # sets bit 6, doesn't clear others
    (0b00001000, CJMode.ENABLE.value, 0b00000000),          # clears bit 3, doesn't set others
    (0b00000000, CJMode.ENABLE.value, 0b00000000),          # doesn't toggle bit 3
    (0b11111111, CJMode.ENABLE.value, 0b11110111),          # clears bit 3, doesn't clear others
    (0b00000000, CJMode.DISABLE.value, 0b00001000),         # sets bit 3, doesn't set others
    (0b00001000, CJMode.DISABLE.value, 0b00001000),         # doesn't toggle bit 3
    (0b11111111, CJMode.DISABLE.value, 0b11111111),         # sets bit 3, doesn't clear others
    (0b00000100, FaultMode.COMPARATOR.value, 0b00000000),   # clears bit 2, doesn't set others
    (0b00000000, FaultMode.COMPARATOR.value, 0b00000000),   # doesn't toggle bit 2
    (0b11111111, FaultMode.COMPARATOR.value, 0b11111011),   # clears bit 2, doesn't clear others
    (0b00000000, FaultMode.INTERRUPT.value, 0b00000100),    # sets bit 2, doesn't set others
    (0b00000100, FaultMode.INTERRUPT.value, 0b00000100),    # doesn't toggle bit 2
    (0b11111011, FaultMode.INTERRUPT.value, 0b11111111),    # sets bit 2, doesn't clear others
    (0b00000000, TCOps.CLEAR_FAULTS.value, 0b00000010),     # sets bit 1, doesn't set others
    (0b00000010, TCOps.CLEAR_FAULTS.value, 0b00000010),     # doesn't toggle bit 1
    (0b11111101, TCOps.CLEAR_FAULTS.value, 0b11111111),     # sets bit 1, doesn't clear others
    (0b00000001, NoiseFilterMode.HZ_60.value, 0b00000000),  # clears bit 0, doesn't set others
    (0b00000000, NoiseFilterMode.HZ_60.value, 0b00000000),  # doesn't toggle bit 0
    (0b11111111, NoiseFilterMode.HZ_60.value, 0b11111110),  # clears bit 0, doesn't clear others
    (0b00000000, NoiseFilterMode.HZ_50.value, 0b00000001),  # sets bit 0, doesn't set others
    (0b00000001, NoiseFilterMode.HZ_50.value, 0b00000001),  # doesn't toggle bit 0
    (0b11111110, NoiseFilterMode.HZ_50.value, 0b11111111),  # sets bit 0, doesn't clear others
    (0b11110000, AvgMode.AVG_1.value, 0b00000000),          # clears high byte, doesn't set low byte
    (0b00000000, AvgMode.AVG_1.value, 0b00000000),          # doesn't toggle high byte
    (0b11111111, AvgMode.AVG_1.value, 0b00001111),          # clears high byte, doesn't clear low byte
    (0b00000000, AvgMode.AVG_2.value, 0b00010000),          # only sets intended high byte bits
    (0b00010000, AvgMode.AVG_2.value, 0b00010000),          # doesn't toggle intended high byte bits
    (0b11101111, AvgMode.AVG_2.value, 0b00011111),          # only clears intended high byte bits
    (0b00000000, AvgMode.AVG_4.value, 0b00100000),          # only sets high byte bits
    (0b00100000, AvgMode.AVG_4.value, 0b00100000),          # doesn't toggle intended high byte bits
    (0b11011111, AvgMode.AVG_4.value, 0b00101111),          # only clears intended high byte bits
    (0b00000000, AvgMode.AVG_8.value, 0b00110000),          # only sets high byte bits
    (0b00110000, AvgMode.AVG_8.value, 0b00110000),          # doesn't toggle high byte bits
    (0b11001111, AvgMode.AVG_8.value, 0b00111111),          # only clears high byte bits
    (0b00000000, AvgMode.AVG_16.value, 0b01000000),         # only sets high byte bits
    (0b01000000, AvgMode.AVG_16.value, 0b01000000),         # doesn't toggle high byte bits
    (0b10111111, AvgMode.AVG_16.value, 0b01001111),         # only clears high byte bits
    (0b00001111, TCType.TYPE_B.value, 0b00000000),          # clears low byte, doesn't set high byte
    (0b00000000, TCType.TYPE_B.value, 0b00000000),          # doesn't toggle low byte
    (0b11111111, TCType.TYPE_B.value, 0b11110000),          # clears low byte, doesn't clear high byte
    (0b00000000, TCType.TYPE_E.value, 0b00000001),          # only sets low byte bits
    (0b00000001, TCType.TYPE_E.value, 0b00000001),          # doesn't toggle low byte
    (0b11111110, TCType.TYPE_E.value, 0b11110001),          # only clears low byte bits
    (0b00000000, TCType.TYPE_J.value, 0b00000010),          # only sets low byte bits
    (0b00000010, TCType.TYPE_J.value, 0b00000010),          # doesn't toggle low byte
    (0b11111101, TCType.TYPE_J.value, 0b11110010),          # only clears low byte bits
    (0b00000000, TCType.TYPE_K.value, 0b00000011),          # only sets low byte bits
    (0b00000011, TCType.TYPE_K.value, 0b00000011),          # doesn't toggle low byte
    (0b11111100, TCType.TYPE_K.value, 0b11110011),          # only clears low byte bits
    (0b00000000, TCType.TYPE_N.value, 0b00000100),          # only sets low byte bits
    (0b00000100, TCType.TYPE_N.value, 0b00000100),          # doesn't toggle low byte
    (0b11111011, TCType.TYPE_N.value, 0b11110100),          # only clears low byte bits
    (0b00000000, TCType.TYPE_R.value, 0b00000101),          # only sets low byte bits
    (0b00000101, TCType.TYPE_R.value, 0b00000101),          # doesn't toggle low byte
    (0b11111010, TCType.TYPE_R.value, 0b11110101),          # only clears low byte bits
    (0b00000000, TCType.TYPE_S.value, 0b00000110),          # only sets low byte bits
    (0b00000110, TCType.TYPE_S.value, 0b00000110),          # doesn't toggle low byte
    (0b11111001, TCType.TYPE_S.value, 0b11110110),          # only clears low byte bits
    (0b00000000, TCType.TYPE_T.value, 0b00000111),          # only sets low byte bits
    (0b00000111, TCType.TYPE_T.value, 0b00000111),          # doesn't toggle low byte
    (0b11111000, TCType.TYPE_T.value, 0b11110111),          # only clears low byte bits
    (0b00000000, VoltageMode.GAIN_8.value, 0b00001000),     # only sets low byte bits
    (0b00001000, VoltageMode.GAIN_8.value, 0b00001000),     # doesn't toggle low byte
    (0b11110111, VoltageMode.GAIN_8.value, 0b11111000),     # only clears low byte bits
    (0b00000000, VoltageMode.GAIN_32.value, 0b00001100),    # only sets low byte bits
    (0b00001100, VoltageMode.GAIN_32.value, 0b00001100),    # doesn't toggle low byte
    (0b11110011, VoltageMode.GAIN_32.value, 0b11111100),    # only clears low byte bits
    (0b11111111, OpenCircuitMode.DISABLED.value, 0b11001111), # only clears oc bits
    (0b00000000, OpenCircuitMode.DISABLED.value, 0b00000000), # doesn't toggle oc bits or set other bits
    (0b00000000, OpenCircuitMode.LOW_INPUT_IMPEDANCE.value, 0b00010000), # only sets oc bits
    (0b00010000, OpenCircuitMode.LOW_INPUT_IMPEDANCE.value, 0b00010000), # doesn't toggle oc bits
    (0b11111111, OpenCircuitMode.LOW_INPUT_IMPEDANCE.value, 0b11011111), # doesn't clear other bits
    (0b00000000, OpenCircuitMode.MED_INPUT_IMPEDANCE.value, 0b00100000), # only sets oc bits
    (0b00100000, OpenCircuitMode.MED_INPUT_IMPEDANCE.value, 0b00100000), # doesn't toggle oc bits
    (0b11111111, OpenCircuitMode.MED_INPUT_IMPEDANCE.value, 0b11101111), # doesn't clear other bits
    (0b00000000, OpenCircuitMode.HIGH_INPUT_IMPEDANCE.value, 0b00110000), # only sets oc bits
    (0b00110000, OpenCircuitMode.HIGH_INPUT_IMPEDANCE.value, 0b00110000), # doesn't toggle oc bits
    (0b11111111, OpenCircuitMode.HIGH_INPUT_IMPEDANCE.value, 0b11111111), # doesn't clear other bits
])
def test_apply_opcode(reg_value, opcode, updated_reg_value):
    assert _apply_opcode(reg_value, opcode) == updated_reg_value

@pytest.mark.parametrize('reg_values', [
    ({0x0: {'value':0x255}}),
    ({
        0x0: {'value':0x255},
        0x1: {'value':0x255},
        0x2: {'value':0x255}}),
    ({
        0x0: {},
        0x1: {'value':0x255},
        0x2: {}}),
])
def test_add_change_flags_adds_flags(reg_values):
    _add_change_flags(reg_values)
    for key in reg_values:
        assert reg_values[key]['is_changed'] == False

@pytest.mark.parametrize('reg_values, opcodes', [
    ({}, []),
    ({0x0: {}}, []),
    ({}, [AvgMode.AVG_1]),
])
def test_apply_opcodes_raises(reg_values, opcodes):
    with pytest.raises(Exception) as e:
        apply_opcodes(reg_values, opcodes)
    assert 'register_values and opcodes args must both be non-empty' in str(e.value)

@pytest.mark.parametrize('reg_values, opcodes, out', [
    (
        {TCAddresses.CR1_W.value: 0x0}, [AvgMode.AVG_1.value],
        {TCAddresses.CR1_W.value: {'value': AvgMode.AVG_1.value.op_code, 'is_changed': True}}
    ),
    (
        {
            TCAddresses.CR0_W.value: 0x0,
            TCAddresses.CR1_W.value: 0x0
        },
        [AvgMode.AVG_1.value],
        {
            TCAddresses.CR0_W.value: {'value': 0x0, 'is_changed': False},
            TCAddresses.CR1_W.value: {'value': AvgMode.AVG_1.value.op_code, 'is_changed': True}
        },
    ),
    (
        {
            TCAddresses.CR0_W.value: 0x0,
            TCAddresses.CR1_W.value: 0x0
        },
        [AvgMode.AVG_1.value, ConvMode.AUTO.value],
        {
            TCAddresses.CR0_W.value: {'value': ConvMode.AUTO.value.op_code, 'is_changed': True},
            TCAddresses.CR1_W.value: {'value': AvgMode.AVG_1.value.op_code, 'is_changed': True}
        },
    ),
    (
        {
            TCAddresses.CR0_W.value: 0x0,
            TCAddresses.CR1_W.value: 0x0
        },
        [AvgMode.AVG_1.value, ConvMode.AUTO.value],
        {
            TCAddresses.CR0_W.value: {'value': ConvMode.AUTO.value.op_code, 'is_changed': True},
            TCAddresses.CR1_W.value: {'value': AvgMode.AVG_1.value.op_code, 'is_changed': True}
        },
    )
])
def test_apply_opcodes(reg_values, opcodes, out):
    assert apply_opcodes(reg_values, opcodes) == out

@pytest.mark.parametrize('reg_map', [
    ({TCAddresses.CR0_R.value: 0xFF}),
    ({TCAddresses.CR0_R.value: 0xFF, TCAddresses.CR1_R.value: 0x00, TCAddresses.CJLF_R.value: 0x5F}),
])
def test_convert_values_to_dict(reg_map):
    map_copy = deepcopy(reg_map)
    _convert_values_to_dict(reg_map)
    for key in reg_map:
        assert type(reg_map[key]) is dict               # assert changed format to addx, dict pairs
        assert reg_map[key]['value'] == map_copy[key]   # assert value field in dict, and reg_value copied correctly
