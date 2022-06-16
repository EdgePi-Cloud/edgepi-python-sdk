import pytest
from unittest.mock import patch
from edgepi.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import *

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
