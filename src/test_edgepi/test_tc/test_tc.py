import pytest
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import TCCommands
from edgepi.edgepi_tc import *
from test_edgepi.test_tc.mock_MAX31856 import *

@pytest.fixture(name='tc')
def fixture_init_tc():
    tc = TCCommands()
    return tc

@pytest.mark.parametrize("opcode, register_address", [
    (TCOps.SINGLE_SHOT, TCAddresses.CR0_W),
    (ConvMode.SINGLE, TCAddresses.CR0_W),
    (CJMode.ENABLE, TCAddresses.CR0_W),
    (FaultMode.COMPARATOR, TCAddresses.CR0_W),
    (NoiseFilterMode.Hz_50, TCAddresses.CR0_W),
    (AvgMode.AVG_1, TCAddresses.CR1_W),
    (TCType.TYPE_B, TCAddresses.CR1_W),
    ('invalid-key', None),
])
def test_find_register(opcode, register_address, tc):
    assert tc.find_register(opcode) == register_address

@pytest.mark.parametrize("reg_value, ops_list, write_value", [
    (0x0, [CJMode.DISABLE], 0x8),
    (0x8, [CJMode.ENABLE], 0x0),
    (0x0, [ConvMode.AUTO,CJMode.DISABLE], 0x88),
    (0x88, [ConvMode.SINGLE,CJMode.ENABLE], 0x00)
])
def test_generate_cr0_update(reg_value, ops_list, write_value, tc):
    assert tc.generate_cr0_update(reg_value, ops_list) == write_value

@pytest.mark.parametrize("reg_value, ops_list, error", [
    (0x0, [AvgMode.AVG_16], ValueError)
])
def test_generate_cr0_update_exceptions(reg_value, ops_list, error, tc):
    with pytest.raises(Exception) as e:
        tc.generate_cr0_update(reg_value, ops_list)
    assert e.type is error

@pytest.mark.parametrize("reg_addx, reg_value, updates_list, output_code", [
    (TCAddresses.CR0_W.value, 0x0, [ConvMode.AUTO, CJMode.DISABLE], 0x88),
])
def test_get_update_code(reg_addx, reg_value, updates_list, output_code, tc):
    assert tc.get_update_code(reg_addx, reg_value, updates_list) == output_code

@pytest.mark.parametrize("reg_value, updates, write_value", [
    (0x03, [AvgMode.AVG_8, TCType.TYPE_N], 0x34),
    (0x34, [AvgMode.AVG_16], 0x44),
    (0x03, [TCType.TYPE_B], 0x00),
    (0x03, [AvgMode.AVG_16, VoltageMode.GAIN_32], 0x4C)
])
def test_generate_cr1_update(reg_value, updates, write_value, tc):
    assert tc.generate_cr1_update(reg_value, updates) == write_value

# TODO: these tests for exception type seem to not be checking for the raised exception type,
# test-case #3 does not raise ValueError as this edge-case is not handled yet. 
@pytest.mark.parametrize("reg_value, updates", [
    (0x03, [TCType.TYPE_E, TCType.TYPE_N]),
    (0x03, [TCType.TYPE_E, AvgMode.AVG_16, VoltageMode.GAIN_32]),
    (0x03, [TCType.TYPE_N, VoltageMode.GAIN_32])
])
def test_generate_cr1_update_exception(reg_value, updates, tc):
    with pytest.raises(ValueError) as e:
        tc.generate_cr0_update(reg_value, updates)
    assert e.type == ValueError

@pytest.fixture(name='edgepi_tc')
def fixture_init_edgepi_tc():
    edgepi_tc = EdgePiTC()
    return edgepi_tc

@pytest.mark.parametrize("args_list, reg_updates_map", [
    ([CJMode.DISABLE, AvgMode.AVG_16, ConvMode.AUTO],
        {TCAddresses.CR0_W: [CJMode.DISABLE, ConvMode.AUTO], TCAddresses.CR1_W: [AvgMode.AVG_16]}),
    ([CJMode.DISABLE, None, AvgMode.AVG_16, None, ConvMode.AUTO, None],
        {TCAddresses.CR0_W: [CJMode.DISABLE, ConvMode.AUTO], TCAddresses.CR1_W: [AvgMode.AVG_16]}),
    ([None], {}),                                                
])
def test_map_updates_to_address(args_list, reg_updates_map, edgepi_tc):
    assert edgepi_tc.map_updates_to_address(args_list) == reg_updates_map

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
    assert mock_read_num_registers(TCAddresses.CR0_R.value) == [TCAddresses.CR0_R.value] + reg_values

def test_mock_read_registers_to_map():
    assert mock_read_registers_to_map() == mock_register_values
