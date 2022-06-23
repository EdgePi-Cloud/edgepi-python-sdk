import pytest
from unittest.mock import patch
from bitstring import Bits
from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import TCAddresses
from edgepi.tc.tc_faults import FaultMsg, FaultType, Fault, map_fault_status

@pytest.fixture(name='tc')
def fixture_test_edgepi_tc(mocker):
    mocker.patch('edgepi.peripherals.spi.SPI')
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
    mocker.patch('edgepi.peripherals.spi.SpiDevice.transfer')
    mocker.patch('edgepi.tc.edgepi_tc.Bits')
    with patch('edgepi.tc.edgepi_tc.map_fault_status', return_value=pre_filter_map):
        result = tc.read_faults(filter_at_fault=filter_at_fault)
        assert  result == expected
