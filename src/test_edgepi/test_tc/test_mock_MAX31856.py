import  pytest
from edgepi.edgepi_tc import *
from test_edgepi.test_tc.mock_MAX31856 import *

@pytest.fixture(name='edgepi_tc')
def fixture_init_edgepi_tc():
    edgepi_tc = EdgePiTC()
    return edgepi_tc

@pytest.mark.parametrize("data, out", [
    ([TCAddresses.CR0_R.value, 0xFF], [TCAddresses.CR0_R.value, 0x00]),
    ([TCAddresses.CJHF_R.value, 0xFF], [TCAddresses.CJHF_R.value, 0x7F]),
    ([TCAddresses.SR_R.value, 0xFF], [TCAddresses.SR_R.value, 0x00]),
    ([TCAddresses.CR0_R.value]+[0xAA]*3, [TCAddresses.CR0_R.value, 0x00, 0x03, 0xFF]),
    ([TCAddresses.CR0_R.value]+[0xAA]*16, 
        [TCAddresses.CR0_R.value] + list(mock_register_values.values())),
    ([TCAddresses.CJHF_R.value]+[0xAA]*3, [TCAddresses.CJHF_R.value, 0x7F, 0xC0, 0x7F]),
])
def test_mock_MAX31856_transfer(data, out):
    assert mock_MAX31856_transfer(data) == out

@pytest.mark.parametrize("reg_addx, reg_value", [
    (TCAddresses.CR0_R.value, [TCAddresses.CR0_R.value, mock_register_values.get(TCAddresses.CR0_R.value)]),
    (TCAddresses.CR1_R.value, [TCAddresses.CR1_R.value, mock_register_values.get(TCAddresses.CR1_R.value)]),
])
def test_mock_read_register(reg_addx, reg_value):
    assert mock_read_register(reg_addx) == reg_value

def test_mock_read_num_registers():
    reg_values = list(mock_register_values.values())
    assert mock_read_registers(TCAddresses.CR0_R.value) == [TCAddresses.CR0_R.value] + reg_values

def test_mock_read_registers_to_map():
    assert mock_read_registers_to_map() == mock_register_values
