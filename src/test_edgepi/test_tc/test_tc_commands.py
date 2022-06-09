import pytest
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import TCCommands

@pytest.fixture(name='tc')
def fixture_init_tc():
    tc = TCCommands()
    return tc

@pytest.mark.parametrize('code_bytes, temps', [
    ([0x0D, 0x88, 0x00, 0xC0, 0x00, 0x00], (-8, -1024)), # negative temps
    ([0x0D, 0x08, 0x00, 0x40, 0x00, 0x00], (8, 1024)), # positive temps
    ([0x0D, 0x7F, 0xFC, 0x7F, 0xFF, 0xE0], (127.984375, 2047.9921875)), # max temp values
    ([0x0D, 0xFF, 0xFC, 0xFF, 0xFF, 0xE0], (-127.984375, -2047.9921875)), # min temp values
])
def test_code_to_temp(code_bytes, temps, tc):
    assert tc.code_to_temp(code_bytes) == temps
