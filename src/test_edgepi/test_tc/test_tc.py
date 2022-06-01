import pytest
import edgepi
from edgepi import edgepi_tc
from edgepi.tc.tc_constants import *
from edgepi.tc.tc_commands import TCCommands
from edgepi.edgepi_tc import *
from contextlib import nullcontext as does_not_raise

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

@pytest.mark.parametrize("reg_value, ops_list, write_value, exception", [
    (0x0, [CJMode.DISABLE], 0x8, does_not_raise()),
    (0x8, [CJMode.ENABLE], 0x0, does_not_raise()),
    (0x0, [ConvMode.AUTO,CJMode.DISABLE], 0x88, does_not_raise()),
    (0x88, [ConvMode.SINGLE,CJMode.ENABLE], 0x00, does_not_raise()),
    (0x0, [AvgMode.AVG_16], 0x0, pytest.raises(ValueError))
])
def test_generate_cr0_update(reg_value, ops_list, write_value, exception, tc):
    with exception:
        assert tc.generate_cr0_update(reg_value, ops_list) == write_value

@pytest.mark.parametrize("reg_addx, reg_value, updates_list, output_code", [
    (TCAddresses.CR0_W, 0x0, [ConvMode.AUTO, CJMode.DISABLE], 0x88),
])
def test_get_update_code(reg_addx, reg_value, updates_list, output_code, tc):
    assert tc.get_update_code(reg_addx, reg_value, updates_list) == output_code

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

def mock_MAX31856_transfer(data):
    ''' mocks SPI transfer of register data from MAX31856 
    Returns:
        a list of register values starting from start address (data[0]).
    '''
    mock_register_values = {
                            TCAddresses.CR0_R.value: 0x00,
                            TCAddresses.CR1_R.value: 0x03,
                            TCAddresses.MASK_R.value: 0xFF,
                            TCAddresses.CJHF_R.value: 0x7F,
                            TCAddresses.CJLF_R.value: 0xC0,
                            TCAddresses.LTHFTH_R.value: 0x7F,
                            TCAddresses.LTHFTL_R.value: 0xFF,
                            TCAddresses.LTLFTH_R.value: 0x80,
                            TCAddresses.LTLFTL_R.value: 0x00,
                            TCAddresses.CJTO_R.value: 0x00, 
                            TCAddresses.CJTH_R.value: 0x00,
                            TCAddresses.CJTL_R.value: 0x00,
                            TCAddresses.LTCBH_R.value: 0x00,
                            TCAddresses.LTCBM_R.value: 0x00,
                            TCAddresses.LTCBL_R.value: 0x00,
                            TCAddresses.SR_R.value: 0x00,
                            }
    if not data:
        raise ValueError('Cannot transfer empty data container')
    elif len(data) < 2:
        raise ValueError('Only address provided, no read bytes specified')

    out_data = data
    bytes_to_read = len(data) - 1
    reg_addx = data[0].value # start address 
    reg_index = 1
    while bytes_to_read > 0:
        out_data[reg_index] = mock_register_values.get(reg_addx)
        reg_index += 1
        reg_addx += 1
        bytes_to_read -= 1
    return out_data

@pytest.mark.parametrize("data, out", [
    ([TCAddresses.CR0_R, 0xFF], [TCAddresses.CR0_R, 0x00]),
    ([TCAddresses.CJHF_R, 0xFF], [TCAddresses.CJHF_R, 0x7F]),
    ([TCAddresses.SR_R, 0xFF], [TCAddresses.SR_R, 0x00]),
    ([TCAddresses.CR0_R]+[0xAA]*3, [TCAddresses.CR0_R, 0x00, 0x03, 0xFF]),
    ([TCAddresses.CR0_R]+[0xAA]*16, 
        [TCAddresses.CR0_R, 0x00, 0x03, 0xFF, 0x7F, 0xC0, 0x7F, 0xFF, 0x80, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    ([TCAddresses.CJHF_R]+[0xAA]*3, [TCAddresses.CJHF_R, 0x7F, 0xC0, 0x7F]),
])
def test_mock_MAX31856_transfer(data, out):
    assert mock_MAX31856_transfer(data) == out
    