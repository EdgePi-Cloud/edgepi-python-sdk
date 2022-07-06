import pytest
from bitstring import BitArray
from collections import Counter
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import TempType, code_to_temp, _negative_temp_check, tempcode_to_opcode, TempCode

@pytest.mark.parametrize('code_bytes, temps', [
    ([0x0D, 0x88, 0x00, 0xC0, 0x00, 0x00], (-8, -1024)), # negative temps
    ([0x0D, 0x08, 0x00, 0x40, 0x00, 0x00], (8, 1024)), # positive temps
    ([0x0D, 0x7F, 0xFC, 0x7F, 0xFF, 0xE0], (127.984375, 2047.9921875)), # max temp values
    ([0x0D, 0xFF, 0xFC, 0xFF, 0xFF, 0xE0], (-127.984375, -2047.9921875)), # min temp values
    ([0x0D, 0x00, 0x00, 0x00, 0x00, 0x00], (0, 0)), # zero temp
    ([0x0D, 0x15, 0x00, 0x01, 0x50, 0x00], (21, 21)), # room temperature values
])
def test_code_to_temp(code_bytes, temps):
    assert code_to_temp(code_bytes) == temps

@pytest.mark.parametrize('code_bytes, err_type', [
    ([0x0D], IndexError), # should raise IndexError
    ([0x0D, 'hello', 'world', '!', 0x0F, 0x0F], ValueError), # should raise ValueError
])
def test_code_to_temp_exceptions(code_bytes, err_type):
    with pytest.raises(Exception) as e:
        code_to_temp(code_bytes)
    assert e.type == err_type

@pytest.mark.parametrize('temp_code, out, new_value', [
    (BitArray(uint=0b10001000, length=8), True, 0b1000),
    (BitArray(uint=0b01001000, length=8), False, 0b01001000)
])
def test_negative_temp_check(temp_code, out, new_value):
   assert _negative_temp_check(temp_code) == out
   assert temp_code.uint == new_value

@pytest.mark.parametrize('tempcode, tc_type, opcode_list', [
    (TempCode(125, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0x7D, TCAddresses.CJHF_W.value, Masks.BYTE_MASK.value)]),   # single register, + value, no dec, no fillers
    (TempCode(-55, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0xB7, TCAddresses.CJHF_W.value, Masks.BYTE_MASK.value)]),   # single register, - value, no dec, no fillers
    (TempCode(0x4, DecBits4.P0_5, 3, 4, 0, TCAddresses.CJTO_W.value, TempType.COLD_JUNCTION_OFFSET), TCType.TYPE_K,
        [OpCode(0x48, TCAddresses.CJTO_W.value, Masks.BYTE_MASK.value)]),   # single register, + value, dec, no fillers
    (TempCode(-0x4, DecBits4.P0_5, 3, 4, 0, TCAddresses.CJTO_W.value, TempType.COLD_JUNCTION_OFFSET), TCType.TYPE_K,
        [OpCode(0xC8, TCAddresses.CJTO_W.value, Masks.BYTE_MASK.value)]),   # single register, - value, dec, no fillers
    (TempCode(1024, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE), TCType.TYPE_K,
        [OpCode(0x40, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x00, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, - value, no dec, no fillers
    (TempCode(-50, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE), TCType.TYPE_K,
        [OpCode(0x83, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x20, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, - value, no dec, no fillers
    (TempCode(1024, DecBits4.P0_75, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE), TCType.TYPE_K,
        [OpCode(0x40, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x0C, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, + value, dec, no fillers
    (TempCode(-50, DecBits4.P0_75, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE), TCType.TYPE_K,
        [OpCode(0x83, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x2C, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, - value, dec, no fillers
    (TempCode(1372, DecBits4.P0_9375, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE), TCType.TYPE_K,
        [OpCode(0x55, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0xCF, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, max + value, dec, no fillers
    (TempCode(64, DecBits6.P0_296875, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0x40, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x4C, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, + value, dec, fillers
    (TempCode(-8, DecBits6.P0_296875, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0x88, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x4C, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, - value, dec, fillers
    (TempCode(125, DecBits6.P0_984375, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0x7D, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0xFC, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, max + value, dec, fillers
    (TempCode(1, DecBits6.P0_015625, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0x01, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x04, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, min + value, dec, fillers
    (TempCode(0, DecBits6.P0, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0x00, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x00, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, zero value, dec, fillers
    (TempCode(-1, DecBits6.P0_015625, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0x81, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x04, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, max - value, dec, fillers
    (TempCode(-25, DecBits6.P0_984375, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K,
        [OpCode(0x99, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0xFC, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, min - value, dec, fillers
    (TempCode(None, None, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K, [])
])
def test_tempcode_to_opcode(tempcode, tc_type, opcode_list):
    result = tempcode_to_opcode(tempcode, tc_type)
    assert Counter(result) == Counter(opcode_list)

@pytest.mark.parametrize('tempcode, tc_type, err_type', [
    (TempCode(0x7F, DecBits4.P0, 8, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K, ValueError),
    (TempCode(0x7F, DecBits4.P0, 7, 1, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K, ValueError),
    (None, TCType.TYPE_K, ValueError),
    (TempCode(None, DecBits6.P0, 7, 6, 2, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K, ValueError),
    (TempCode(1000, None, 7, 6, 2, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), TCType.TYPE_K, ValueError),
])
def test_tempcode_to_opcode_raises(tempcode, tc_type, err_type):
    with pytest.raises(Exception) as e:
        tempcode_to_opcode(tempcode, tc_type)
    assert e.type == err_type
