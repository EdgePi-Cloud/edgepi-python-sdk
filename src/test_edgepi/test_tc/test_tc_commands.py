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

@pytest.mark.parametrize('tempcode, opcode_list', [
    (TempCode(0x7F, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
        [OpCode(0x7F, TCAddresses.CJHF_W.value, Masks.BYTE_MASK.value)]),   # single register, + value, no dec, no fillers
    (TempCode(-0x7F, DecBits4.P0, 7, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION),
        [OpCode(0xFF, TCAddresses.CJHF_W.value, Masks.BYTE_MASK.value)]),   # single register, - value, no dec, no fillers
    (TempCode(0x4, DecBits4.P0_5, 3, 4, 0, TCAddresses.CJTO_W.value, TempType.COLD_JUNCTION_OFFSET),
        [OpCode(0x48, TCAddresses.CJTO_W.value, Masks.BYTE_MASK.value)]),   # single register, + value, dec, no fillers
    (TempCode(-0x4, DecBits4.P0_5, 3, 4, 0, TCAddresses.CJTO_W.value, TempType.COLD_JUNCTION_OFFSET),
        [OpCode(0xC8, TCAddresses.CJTO_W.value, Masks.BYTE_MASK.value)]),   # single register, - value, dec, no fillers
    (TempCode(1024, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE),
        [OpCode(0x40, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x00, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, - value, no dec, no fillers
    (TempCode(-1024, DecBits4.P0, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE),
        [OpCode(0xC0, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x00, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, - value, no dec, no fillers
    (TempCode(1024, DecBits4.P0_75, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE),
        [OpCode(0x40, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x0C, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, + value, dec, no fillers
    (TempCode(-1024, DecBits4.P0_75, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE),
        [OpCode(0xC0, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x0C, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, - value, dec, no fillers
    (TempCode(2047, DecBits4.P0_9375, 11, 4, 0, TCAddresses.LTHFTH_W.value, TempType.THERMOCOUPLE),
        [OpCode(0x7F, TCAddresses.LTHFTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0xFF, TCAddresses.LTHFTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, max + value, dec, no fillers
    (TempCode(64, DecBits6.P0_296875, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
        [OpCode(0x40, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x4C, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, + value, dec, fillers
    (TempCode(-64, DecBits6.P0_296875, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
        [OpCode(0xC0, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x4C, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, - value, dec, fillers
    (TempCode(127, DecBits6.P0_984375, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
        [OpCode(0x7F, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0xFC, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, max + value, dec, fillers
    (TempCode(1, DecBits6.P0_015625, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
        [OpCode(0x01, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x04, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, min + value, dec, fillers
    (TempCode(0, DecBits6.P0, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
        [OpCode(0x00, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x00, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, zero value, dec, fillers
    (TempCode(-1, DecBits6.P0_015625, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
        [OpCode(0x81, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0x04, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, max - value, dec, fillers
    (TempCode(-127, DecBits6.P0_984375, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION),
        [OpCode(0xFF, TCAddresses.CJTH_W.value, Masks.BYTE_MASK.value),
        OpCode(0xFC, TCAddresses.CJTL_W.value, Masks.BYTE_MASK.value)]),   # 2 registers, min - value, dec, fillers
    (TempCode(None, None, 7, 6, 2, TCAddresses.CJTH_W.value, TempType.COLD_JUNCTION), [])
])
def test_tempcode_to_opcode(tempcode, opcode_list):
    result = tempcode_to_opcode(tempcode)
    assert Counter(result) == Counter(opcode_list)

@pytest.mark.parametrize('tempcode, err_type', [
    (TempCode(0x7F, DecBits4.P0, 8, 0, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), ValueError),
    (TempCode(0x7F, DecBits4.P0, 7, 1, 0, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), ValueError),
    (None, ValueError),
    (TempCode(None, DecBits6.P0, 7, 6, 2, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), ValueError),
    (TempCode(1000, None, 7, 6, 2, TCAddresses.CJHF_W.value, TempType.COLD_JUNCTION), ValueError),
])
def test_tempcode_to_opcode_raises(tempcode, err_type):
    with pytest.raises(Exception) as e:
        tempcode_to_opcode(tempcode)
    assert e.type == err_type
