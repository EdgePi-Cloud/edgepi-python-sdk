'''unit test for access eeprom'''

from unittest import mock
from unittest.mock import patch
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.peripherals.i2c import I2CDevice
from edgepi.calibration.access_eeprom import (
    selective_read,
    sequential_read,
    byte_write_register,
    page_write_register
)

@pytest.fixture(name="bus")
def fixture_test_dac(mocker):
    mocker.patch("edgepi.peripherals.i2c.I2C")
    yield I2CDevice('/dev/i2c-10')

@pytest.mark.parametrize("reg_addr, dev_addr, mock_val, result", [(1, 32, [23], [23])])
def test_selective_read(mocker, bus, reg_addr, dev_addr, mock_val, result):
    mock_set_msg = mocker.patch("edgepi.peripherals.i2c.I2CDevice.transfer",return_value = mock_val)
    read_result = selective_read(bus, reg_addr, dev_addr)
    assert read_result == result



@pytest.mark.parametrize("reg_addr, length, dev_addr, mock_val, result", [(1, 5, 32, [23, 34, 56, 7, 8], [23, 34, 56, 7, 8])])
def test_sequential_read(mocker, bus, reg_addr, length, dev_addr, mock_val, result):
    mock_set_msg = mocker.patch("edgepi.peripherals.i2c.I2CDevice.transfer",return_value = mock_val)
    read_result = sequential_read(bus, reg_addr, length, dev_addr)
    assert read_result == result