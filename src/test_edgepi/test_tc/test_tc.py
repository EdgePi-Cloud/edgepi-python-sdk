import pytest
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import TCCommands, register_write_map

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
    assert tc.find_register(opcode, register_write_map) == register_address
