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

@pytest.mark.parametrize("reg_addr, dev_addr, result", [(1, 32, 1)])
def test_selective_read(mocker, bus, reg_addr, dev_addr, result):
    mock_msg = mocker.patch("edgepi.peripherals.i2c.I2CDevice.Message", side_effect = [reg_addr, 255])
    mock_msg.return_value = (mock_msg, mock_msg)
    selective_read(bus, reg_addr, dev_addr)
    check = result