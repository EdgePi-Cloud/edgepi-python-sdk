import pytest
from copy import deepcopy
from unittest.mock import call, patch
from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import AvgMode, DecBits4, DecBits6, TCAddresses
from edgepi.tc.tc_faults import FaultMsg, FaultType, Fault

@pytest.fixture(name='tc')
def fixture_test_edgepi_tc(mocker):
    mocker.patch('edgepi.tc.edgepi_tc.SpiDevice')
    return EdgePiTC()

@pytest.mark.parametrize('reg_address, data', [
    (TCAddresses.CR0_R.value, [TCAddresses.CR0_R.value, 0xFF]),
    (TCAddresses.CR0_W.value, [TCAddresses.CR0_W.value, 0xFF]),
    (TCAddresses.CR1_R.value, [TCAddresses.CR1_R.value, 0xFF]),
    (TCAddresses.CR1_W.value, [TCAddresses.CR1_W.value, 0xFF]),
])
@patch('edgepi.peripherals.spi.SpiDevice.transfer')
def test_read_register_passes_data(mock_transfer, reg_address, data, tc):
    tc._EdgePiTC__read_register(reg_address)
    mock_transfer.assert_called_once_with(data)

@pytest.mark.parametrize('reg_address, out', [
    (TCAddresses.CR0_R.value, [TCAddresses.CR0_R.value, 0x0]),
    (TCAddresses.CR0_W.value, [TCAddresses.CR0_W.value, 0x0]),
    (TCAddresses.CR1_R.value, [TCAddresses.CR1_R.value, 0x3]),
    (TCAddresses.CR1_W.value, [TCAddresses.CR1_W.value, 0x3]),
])
def test_read_register_returns_data(mocker, reg_address, out, tc):
    mocker.patch('edgepi.peripherals.spi.SpiDevice.transfer', return_value=out)
    out_data = tc._EdgePiTC__read_register(reg_address)
    assert out_data == out

@pytest.mark.parametrize('reg_address, value', [
    (TCAddresses.CR0_W.value, 0xFF),
    (TCAddresses.CR1_W.value, 0xFF),
])
@patch('edgepi.peripherals.spi.SpiDevice.transfer')
def test_write_to_register_passes_data(mock_transfer, reg_address, value, tc):
    tc._EdgePiTC__read_register(reg_address)
    data = [reg_address] + [value]
    mock_transfer.assert_called_once_with(data)

@pytest.mark.parametrize('filter_at_fault, pre_filter_map, expected', [
    (True,
        {FaultType.OPEN:Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)},
        {}
    ),  # no faults, return only asserting faults
    (False,
        {FaultType.OPEN:Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)},
        {FaultType.OPEN:Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)}
    ),  # no faults, return all faults
    (True,
        {
            FaultType.OVUV:Fault(FaultType.OVUV, FaultMsg.OVUV_OK_MSG, True, True),
            FaultType.OPEN:Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)
        },
        {FaultType.OVUV:Fault(FaultType.OVUV, FaultMsg.OVUV_OK_MSG, True, True)}
    ),  # all faults, return only asserting faults
    (False,
        {
            FaultType.OVUV:Fault(FaultType.OVUV, FaultMsg.OVUV_OK_MSG, True, True),
            FaultType.OPEN:Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)
        },
        {
            FaultType.OVUV:Fault(FaultType.OVUV, FaultMsg.OVUV_OK_MSG, True, True),
            FaultType.OPEN:Fault(FaultType.OPEN, FaultMsg.OPEN_OK_MSG, False, True)
        }
    ),  # all faults, return all faults
])
def test_read_faults_filters(mocker, filter_at_fault, pre_filter_map, expected, tc):
    mocker.patch('edgepi.tc.edgepi_tc.Bits')
    with patch('edgepi.tc.edgepi_tc.map_fault_status', return_value=pre_filter_map):
        result = tc.read_faults(filter_at_fault=filter_at_fault)
        assert  result == expected

default_reg_values = {
    TCAddresses.CR0_W.value: 0x0,
    TCAddresses.CR1_W.value: 0x0,
    TCAddresses.MASK_W.value: 0x0,
    TCAddresses.CJHF_W.value: 0x0,
    TCAddresses.CJLF_W.value: 0x0,
    TCAddresses.LTHFTH_W.value: 0x0,
    TCAddresses.LTHFTL_W.value: 0x0,
    TCAddresses.LTLFTH_W.value: 0x0,
    TCAddresses.LTLFTL_W.value: 0x0,
    TCAddresses.CJTO_W.value: 0x0,
    TCAddresses.CJTH_W.value: 0x0,
    TCAddresses.CJTL_W.value: 0x0
}

@pytest.mark.parametrize('args, reg_values, updated_regs', [
    ({'average_mode': AvgMode.AVG_16}, deepcopy(default_reg_values), {TCAddresses.CR1_W.value: 0x40}),
    ({'average_mode': AvgMode.AVG_8}, deepcopy(default_reg_values), {TCAddresses.CR1_W.value: 0x30}),
    ({'average_mode': AvgMode.AVG_4}, deepcopy(default_reg_values), {TCAddresses.CR1_W.value: 0x20}),
    ({'average_mode': AvgMode.AVG_2}, deepcopy(default_reg_values), {TCAddresses.CR1_W.value: 0x10}),
    ({'average_mode': AvgMode.AVG_1}, deepcopy(default_reg_values), {TCAddresses.CR1_W.value: 0x0}),
    ({'cj_high_threshold': 100}, deepcopy(default_reg_values), {TCAddresses.CJHF_W.value: 0x64}),
    ({'cj_low_threshold': -100}, deepcopy(default_reg_values), {TCAddresses.CJLF_W.value: 0xE4}),
    ({'lt_high_threshold': 1000, 'lt_high_threshold_decimals': DecBits4.P0_9375}, deepcopy(default_reg_values),
        {
            TCAddresses.LTHFTH_W.value: 0x3E,
            TCAddresses.LTHFTL_W.value: 0x8F
        }),
    ({'lt_low_threshold': -1000, 'lt_low_threshold_decimals': DecBits4.P0_9375}, deepcopy(default_reg_values),
        {
            TCAddresses.LTLFTH_W.value: 0xBE,
            TCAddresses.LTLFTL_W.value: 0x8F
        }),
    ({'cj_offset': 4, 'cj_offset_decimals': DecBits4.P0_9375}, deepcopy(default_reg_values),
        {
            TCAddresses.CJTO_W.value: 0x4F,
        }),
    ({'cj_temp': 100, 'cj_temp_decimals': DecBits6.P0_984375}, deepcopy(default_reg_values),
        {
            TCAddresses.CJTH_W.value: 0x64,
            TCAddresses.CJTL_W.value: 0xFC
        }),
])
def test_set_config(mocker, args, reg_values, updated_regs, tc):
    # insert mock register values -- set_config will update these with opcodes
    mocker.patch('edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__read_registers_to_map', return_value=reg_values)
    tc.set_config(**args)

    for addx, entry in reg_values.items():
        # check registers not updated have not been changed
        if addx not in updated_regs:
            assert entry['is_changed'] == False
            assert entry['value'] == default_reg_values[addx]
        # check updates were applied
        else:
            assert reg_values[addx]['value'] == updated_regs[addx]
            assert reg_values[addx]['is_changed'] == True

@pytest.mark.parametrize('reg_values', [
    ({TCAddresses.CR0_W.value: {'is_changed': True, 'value': 0xFF}}),
    ({
        TCAddresses.CR0_W.value: {'is_changed': True, 'value': 0xFF},
        TCAddresses.CR1_W.value: {'is_changed': True, 'value': 0xFF}}),
    ({TCAddresses.CR0_W.value: {'is_changed': False, 'value': 0xFF}}),
    ({
        TCAddresses.CR0_W.value: {'is_changed': True, 'value': 0xFF},
        TCAddresses.CR1_W.value: {'is_changed': True, 'value': 0xFF}}),
    ({
        TCAddresses.CR0_W.value: {'is_changed': True, 'value': 0xFF},
        TCAddresses.CR1_W.value: {'is_changed': True, 'value': 0xFF},
        TCAddresses.CJHF_W.value: {'is_changed': False, 'value': 0x0}}),
])
@patch('edgepi.tc.edgepi_tc.EdgePiTC._EdgePiTC__write_to_register')
def test_update_registers_from_dict(mock_write, reg_values, tc):
    # construct list of expected calls to __write_to_register
    write_calls = []
    for addx, entry in reg_values.items():
        if entry['is_changed']:
            write_calls.append(call(addx, entry['value']))

    tc._EdgePiTC__update_registers_from_dict(reg_values)

    # assert __write_to_register called with expected calls
    mock_write.assert_has_calls(write_calls, any_order=True)
