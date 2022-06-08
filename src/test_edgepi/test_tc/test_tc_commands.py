import pytest
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import TCCommands

@pytest.fixture(name='tc')
def fixture_init_tc():
    tc = TCCommands()
    return tc
