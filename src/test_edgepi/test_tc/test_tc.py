import pytest
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import TCCommands
from contextlib import nullcontext as does_not_raise

@pytest.fixture(name='tc')
def fixture_init_tc():
    tc = TCCommands()
    return tc

@pytest.mark.parametrize("opcode, register_address", [
    (TC_OPS.SINGLE_SHOT, TC_ADDRESSES.CR0_W),
    (CONV_MODE.SINGLE, TC_ADDRESSES.CR0_W),
    (CJ_MODE.ENABLE, TC_ADDRESSES.CR0_W),
    (FAULT_MODE.COMPARATOR, TC_ADDRESSES.CR0_W),
    (NOISE_FILTER_MODE.Hz_50, TC_ADDRESSES.CR0_W),
    (AVG_MODE.AVG_1, TC_ADDRESSES.CR1_W),
    (TC_TYPE.TYPE_B, TC_ADDRESSES.CR1_W),
    ('invalid-key', None),
])
def test_find_register(opcode, register_address, tc):
    assert tc.find_register(opcode) == register_address

@pytest.mark.parametrize("read_value, ops_list, write_value, exception", [
    (0x0, [CJ_MODE.DISABLE], 0x8, does_not_raise()),
    (0x8, [CJ_MODE.ENABLE], 0x0, does_not_raise()),
    (0x0, [CONV_MODE.AUTO,CJ_MODE.DISABLE], 0x88, does_not_raise()),
    (0x88, [CONV_MODE.SINGLE,CJ_MODE.ENABLE], 0x00, does_not_raise()),
    (0x0, [AVG_MODE.AVG_16], 0x0, pytest.raises(ValueError))
])
def test_generate_cr0_update(read_value, ops_list, write_value, exception, tc):
    with exception:
        assert tc.generate_cr0_update(read_value, ops_list) == write_value