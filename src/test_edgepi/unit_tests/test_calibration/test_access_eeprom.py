'''unit test for access eeprom'''

# pylint: disable=C0413


from unittest import mock
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM

@pytest.fixture(name="eeprom")
def fixture_test_dac(mocker):
    mocker.patch("edgepi.peripherals.i2c.I2C")
    yield EdgePiEEPROM()

@pytest.mark.parametrize("reg_addr, mock_val, result", [(1, [23], [23])])
def test_selective_read(mocker, eeprom, reg_addr, mock_val, result):
    mocker.patch("edgepi.peripherals.i2c.I2CDevice.transfer",return_value = mock_val)
    read_result = eeprom.selective_read(reg_addr)
    assert read_result == result



@pytest.mark.parametrize("reg_addr, length, mock_val, result", [(1, 5,
                                                                [23, 34, 56, 7, 8],
                                                                [23, 34, 56, 7, 8])])
def test_sequential_read(mocker, eeprom, reg_addr, length, mock_val, result):
    mocker.patch("edgepi.peripherals.i2c.I2CDevice.transfer",return_value = mock_val)
    read_result = eeprom.sequential_read( reg_addr, length)
    assert read_result == result
