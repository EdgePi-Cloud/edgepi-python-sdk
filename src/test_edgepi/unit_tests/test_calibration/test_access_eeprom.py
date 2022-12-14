'''unit test for access eeprom'''

# pylint: disable=C0413


from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.calibration.eeprom_constants import MessageFieldNumber
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout

@pytest.fixture(name="eeprom")
def fixture_test_dac(mocker):
    mocker.patch("edgepi.peripherals.i2c.I2C")
    yield EdgePiEEPROM()

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/serializedFile","rb") as fd:
        b_string = fd.read()
    return b_string

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

def test__read_edgepi_reserved_memory(mocker, eeprom):
    # pylint: disable=protected-access
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__allocated_memory")
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM.sequential_read",
                return_value =list(read_binfile()))
    byte_string = eeprom._EdgePiEEPROM__read_edgepi_reserved_memory()
    assert byte_string == read_binfile()

@pytest.mark.parametrize("msg",
                        [(MessageFieldNumber.DAC),
                         (MessageFieldNumber.ADC),
                         (MessageFieldNumber.RTD),
                         (MessageFieldNumber.TC),
                         (MessageFieldNumber.CONFIGS_KEY),
                         (MessageFieldNumber.DATA_KEY),
                         (MessageFieldNumber.SERIAL),
                         (MessageFieldNumber.MODEL),
                         (MessageFieldNumber.CLIENT_ID)
                        ])
def test_get_message_of_interest(mocker, msg, eeprom):
    # pylint: disable=protected-access
    mocker.patch(
        "edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__read_edgepi_reserved_memory",
        return_value = read_binfile())
    memory_contents = EepromLayout()
    memory_contents.ParseFromString(read_binfile())
    msg_of_interest = eeprom.get_message_of_interest(msg)
    assert msg_of_interest == memory_contents.ListFields()[msg.value -1][1]

def test_get_edgepi_reserved_data(mocker, eeprom):
    # pylint: disable=protected-access
    mocker.patch(
        "edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__read_edgepi_reserved_memory",
        return_value = read_binfile())
    memory_contents = EepromLayout()
    memory_contents.ParseFromString(read_binfile())
    edgepi_eeprom_dataclass = eeprom.get_edgepi_reserved_data()
    assert edgepi_eeprom_dataclass.dac_calib_parms is not None
    assert edgepi_eeprom_dataclass.adc_calib_parms is not None
    assert edgepi_eeprom_dataclass.rtd_calib_parms is not None
    assert edgepi_eeprom_dataclass.tc_calib_parms is not None
    assert edgepi_eeprom_dataclass.config_key is not None
    assert edgepi_eeprom_dataclass.data_key is not None
    assert edgepi_eeprom_dataclass.serial is not None
    assert edgepi_eeprom_dataclass.model is not None
    assert edgepi_eeprom_dataclass.client_id is not None
