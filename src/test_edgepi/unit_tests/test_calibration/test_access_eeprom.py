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

@pytest.mark.parametrize("page_addr, byte_addr, result",
                        [(0, 8, [0x00, 0x08]),
                         (0, 63, [0x00, 0x3F]),
                         (511, 63, [0x7F, 0xFF]),
                         (511, 0, [0x7F, 0xC0])
                        ])
def test__pack_mem_address(page_addr, byte_addr, result, eeprom):
    # pylint: disable=protected-access
    address_message = eeprom._EdgePiEEPROM__pack_mem_address(page_addr, byte_addr)
    assert address_message == result

@pytest.mark.parametrize("memory_address, result",
                        [(0, [0, 0]),
                         (63, [0, 63]),
                         (64, [1, 0]),
                         (32767, [511, 63]),
                         (32704, [511, 0])
                        ])
def test__byte_address_generation(memory_address, result, eeprom):
    # pylint: disable=protected-access
    page_addr, byte_addr = eeprom._EdgePiEEPROM__byte_address_generation(memory_address)
    assert page_addr == result[0]
    assert byte_addr == result[1]

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

@pytest.mark.parametrize("mock_value,result",
                        [([0,123], 123),
                         ([1,1], 257),
                         ([63,255], 16383),
                         ([63, 0], 16128)
                        ])
def test__allocated_memory(mocker,mock_value,result, eeprom):
    # pylint: disable=protected-access
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM.sequential_read",
                return_value =mock_value)
    length = eeprom._EdgePiEEPROM__allocated_memory()
    assert length == result