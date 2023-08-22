'''unit test for access eeprom'''

# pylint: disable=C0413
# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372

from unittest import mock
import base64
import os
PATH = os.path.dirname(os.path.abspath(__file__))
import sys
sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import json
import pytest

from edgepi.utilities.crc_8_atm import CRC_BYTE_SIZE, check_crc, get_crc
from edgepi.eeprom.eeprom_constants import (
    EdgePiMemoryInfo,
    EEPROMInfo,
    DEFAULT_EEPROM_BIN_B64
    )
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM, MemoryOutOfBound, PermissionDenied
from edgepi.eeprom.protobuf_assets.generated_pb2 import edgepi_module_pb2
from edgepi.eeprom.edgepi_eeprom_data import EepromDataClass
from edgepi.calibration.calibration_constants import CalibParam

@pytest.fixture(name="eeprom")
def fixture_test_dac(mocker):
    mocker.patch("edgepi.peripherals.i2c.I2C")
    yield EdgePiEEPROM()

# Max data size of osensa space
OSENSA_DATA_SIZE = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value

# Max size of User space = End of memory - start of memory + 1
USER_SPACE_SIZE = EdgePiMemoryInfo.USER_SPACE_END_BYTE.value -\
                  EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + 1

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/edgepi_default_bin","rb") as fd:
        b_string = fd.read()
    return b_string

def read_dummy_json(file_name: str):
    """Read Jason file"""
    # pylint: disable=unspecified-encoding
    with open(PATH+"/"+file_name, "r") as file:
        dummy = json.load(file)
    return dummy

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

@pytest.mark.parametrize("reg_addr, length, mock_val, result", [(1, 5,
                                                                [23, 34, 56, 7, 8],
                                                                [23, 34, 56, 7, 8])])
def test_sequential_read(mocker, eeprom, reg_addr, length, mock_val, result):
    mocker.patch("edgepi.peripherals.i2c.I2CDevice.transfer",return_value = mock_val)
    # pylint: disable=protected-access
    with eeprom.i2c_open():
        read_result = eeprom._EdgePiEEPROM__sequential_read( reg_addr, length)
    assert read_result == result
    assert eeprom.i2cdev.close.called_once()

@pytest.mark.parametrize("mock_value,result",
                        [([0,123], 123),
                         ([1,1], 257),
                         ([63,255], 16383),
                         ([63, 0], 16128)
                        ])
def test__allocated_memory(mocker,mock_value,result, eeprom):
    data = mock_value + [1]*61
    data = get_crc(data)
    # pylint: disable=protected-access
    mocker.patch("edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
                return_value =data)
    # pylint: disable=protected-access
    length = eeprom._EdgePiEEPROM__allocated_memory(EdgePiMemoryInfo.USED_SPACE.value)
    assert length == result
    assert eeprom.i2cdev.close.called_once()


def test__read_edgepi_reserved_memory(mocker, eeprom):
    data_b = read_binfile()
    # pylint: disable=protected-access
    data_l = eeprom._EdgePiEEPROM__generate_data_list(data_b)
    # pylint: disable=protected-access
    pages = eeprom._EdgePiEEPROM__generate_list_of_pages_crc(data_l)

    # pylint: disable=protected-access
    mocker.patch("edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__allocated_memory",
                 return_value = (data_l[0]<<8) + data_l[1])
    mocker.patch("edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
                side_effect = list(pages))
    # pylint: disable=protected-access
    byte_string = eeprom._EdgePiEEPROM__read_edgepi_reserved_memory()
    assert byte_string == data_b
    # expected call count of close is one due to the mocked __allocated_memory
    assert eeprom.i2cdev.close.called_once()


dac_dict_calib = {0:CalibParam(gain = 1.0229951270016944, offset= -0.01787674545454656),
                  1:CalibParam(gain = 1.0233775195153139, offset= -0.019239763636362414),
                  2:CalibParam(gain = 1.0238480841375301, offset= -0.014646763636360628),
                  3:CalibParam(gain = 1.021600135, offset= -0.0190202),
                  4:CalibParam(gain = 1.022255745463092, offset= -0.0165660727272739),
                  5:CalibParam(gain = 1.0229838854579036, offset= -0.017047454545456923),
                  6:CalibParam(gain = 1.0247617896158834, offset= -0.01857707272727247),
                  7:CalibParam(gain = 1.0208361905168861, offset= -0.016279636363636222)}

adc_dict_calib = {0:CalibParam(gain = 1.0047302081335363, offset= -0.0898128361249185),
                  1:CalibParam(gain = 1.00005219259183, offset= -0.037039036876729624),
                  2:CalibParam(gain = 0.9952694074595573, offset= 0.022449294616625794),
                  3:CalibParam(gain = 0.9930298122067595, offset= 0.052559933743999566),
                  4:CalibParam(gain = 0.9986894662368055, offset= -0.01639367419587856),
                  5:CalibParam(gain = 0.9962817511793706, offset= 0.012169769827208299),
                  6:CalibParam(gain = 0.9977479673435563, offset= -0.006497032357507848),
                  7:CalibParam(gain = 0.9967431970740426, offset= 0.005837911244602978),
                  8:CalibParam(gain = 1.0093016097792906, offset= -0.05178411804847496),
                  9:CalibParam(gain = 0.9977895773887948, offset= -0.030203102327682706),
                  10:CalibParam(gain = 1.0011882603521973, offset= -0.02699318647809985),
                  11:CalibParam(gain = 0.9988614798071136, offset= -0.010834493145652147)}

rtd_dict_calib = {0:CalibParam(gain = 1, offset=0)}
rtd_dict_hw= {0:1}
tc_dict_calib = {0:CalibParam(gain = 1, offset=0)}
tc_dict_hw = {0:1}

def test_read_edgepi_data(mocker, eeprom):
    # pylint: disable=protected-access
    mocker.patch(
        "edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__read_edgepi_reserved_memory",
        return_value = read_binfile())
    # pylint: disable=no-member
    memory_contents = edgepi_module_pb2.EepromData()
    memory_contents.ParseFromString(read_binfile())
    memory_data = EepromDataClass.extract_eeprom_data(memory_contents)
    eeprom_data = eeprom.read_edgepi_data()
    assert memory_data.__dict__ == eeprom_data.__dict__

@pytest.mark.parametrize("size",
                        [
                         (6704),
                         (5000),
                         (9000)
                        ])
def test__generate_data_list(size, eeprom):
    page_size = EEPROMInfo.PAGE_SIZE.value - CRC_BYTE_SIZE
    data = [1]*size
    expected = [(size>>8)&0xFF, size&0xFF] + data + [255]*(page_size - (size+2)%page_size)
    # pylint: disable=protected-access
    data_l = eeprom._EdgePiEEPROM__generate_data_list(data)
    assert data_l == expected

@pytest.mark.parametrize("size, error",
                        [
                         (6704, does_not_raise()),
                         (5000, does_not_raise()),
                         (9000, does_not_raise())
                        ])
def test__generate_list_of_pages_crc(size, error, eeprom):
    data = [1]*size
    # pylint: disable=protected-access
    data_l = eeprom._EdgePiEEPROM__generate_data_list(data)
    # pylint: disable=protected-access
    pages = eeprom._EdgePiEEPROM__generate_list_of_pages_crc(data_l)
    with error:
        for page in pages:
            check_crc(page[:-1], page[-1])

@pytest.mark.parametrize("data_size, error",
                        [
                         (6704, does_not_raise()),
                         (5000, does_not_raise()),
                         (9000, does_not_raise()),
                         (OSENSA_DATA_SIZE, pytest.raises(MemoryOutOfBound)),
                         (OSENSA_DATA_SIZE-256, pytest.raises(MemoryOutOfBound)),
                        ])
def test__write_edgepi_reserved_memory(mocker, data_size, error, eeprom):
    mocker.patch("edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__page_write_register")
    data = bytes([1]*data_size)
    with error:
    # pylint: disable=protected-access
        eeprom._EdgePiEEPROM__write_edgepi_reserved_memory(data)

@pytest.mark.parametrize("mem_address,length, user_space, error",
                        [(0, 5000,True,does_not_raise()),
                         (0, 10000, True,does_not_raise()),
                         (0, USER_SPACE_SIZE-1,True,does_not_raise()),
                         (0, USER_SPACE_SIZE, True,does_not_raise()),
                         (1, USER_SPACE_SIZE, True,pytest.raises(MemoryOutOfBound)),
                         (USER_SPACE_SIZE-1,0,True,pytest.raises(ValueError)),
                         (USER_SPACE_SIZE-1,1,True,does_not_raise()),
                         (USER_SPACE_SIZE-1,2,True,pytest.raises(MemoryOutOfBound)),
                         (USER_SPACE_SIZE-2,1,True,does_not_raise()),
                         (0, 5000, False,does_not_raise()),
                         (0, 10000, False,does_not_raise()),
                         (0, OSENSA_DATA_SIZE, False,does_not_raise()),
                         (1, OSENSA_DATA_SIZE, False,pytest.raises(MemoryOutOfBound)),
                         (2, OSENSA_DATA_SIZE, False, pytest.raises(MemoryOutOfBound)),
                         (OSENSA_DATA_SIZE-1, 0, False,pytest.raises(ValueError)),
                         (OSENSA_DATA_SIZE-1, 1, False,does_not_raise()),
                         (OSENSA_DATA_SIZE-1, 2, False,pytest.raises(MemoryOutOfBound)),
                        ])
def test_parameter_sanity_chekc(mem_address, length, user_space, error, eeprom):
    address = (EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + mem_address) if user_space \
              else mem_address
    with error:
        # pylint: disable=protected-access
        eeprom._EdgePiEEPROM__parameter_sanity_check(address , length, user_space)

# TODO:need to fix this
@pytest.mark.parametrize("json_file_name, error",
                        [("dummy_0.json",does_not_raise()),
                         ("dummy_0.json",does_not_raise()),
                         ])
def test__generate_list_of_pages_json(json_file_name, error,eeprom):
    json_data = read_dummy_json(json_file_name)
    data_b = bytes(json.dumps(json_data,indent=0,sort_keys=False,separators=(',', ':')), "utf-8")
    # pylint: disable=protected-access
    data_l = eeprom._EdgePiEEPROM__generate_data_list(data_b)
    assert data_l[0] == (len(data_b)>>8)&0xFF
    assert data_l[1] == len(data_b)&0xFF
    assert len(data_l)%(EEPROMInfo.PAGE_SIZE.value - CRC_BYTE_SIZE) == 0
    # pylint: disable=protected-access
    page_n = eeprom._EdgePiEEPROM__generate_list_of_pages_crc(data_l)
    with error:
        for page in page_n:
            assert len(page) == EEPROMInfo.PAGE_SIZE.value
            check_crc(page[:-1], page[-1])

def test_read_user_space(mocker, eeprom):
    dummy_data = read_dummy_json("dummy_0.json")
    dummy_data_b = bytes(json.dumps(dummy_data), "utf-8")
    # pylint: disable=protected-access
    dummy_data_l = eeprom._EdgePiEEPROM__generate_data_list(dummy_data_b)
    # pylint: disable=protected-access
    pages = eeprom._EdgePiEEPROM__generate_list_of_pages_crc(dummy_data_l)
    mocker.patch(
        "edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
        side_effect = pages)
    data_size = (dummy_data_l[0]<<8) + dummy_data_l[1]
    result = eeprom.read_user_space(data_size)
    assert result == list(dummy_data_b)
    assert eeprom.i2cdev.close.called_once()

@pytest.mark.parametrize("mem_size, dummy_size, result, error",
                        [(3, 3,[False, False], does_not_raise()),
                         (512, 512, [False, False], does_not_raise()),
                         (0x3FFF, 0, [True, False], pytest.raises(ValueError)),
                         (0x3FFC, 5460, [True, False], does_not_raise()),
                         (0xFFFF, 0, [False, True], does_not_raise()),
                        ])
def test_init_memory(mocker, mem_size, dummy_size, result, error, eeprom):
    mocker.patch(
        "edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM.read_user_space",
        return_value = list(bytes(json.dumps([2]*dummy_size), "utf8")))
    mocker.patch("edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__allocated_memory",
                  return_value = mem_size)
    with error:
        is_full, is_empty = eeprom.init_memory()
        assert is_full == result[0]
        assert is_empty == result[1]
        if not is_full and not is_empty:
            assert eeprom.data_list == [2]*mem_size
            assert eeprom.used_size == mem_size
        elif is_full and not is_empty:
            assert eeprom.data_list == [2]*int(mem_size/3)
            assert eeprom.used_size == mem_size
        else:
            assert eeprom.data_list == []

@pytest.mark.parametrize("bin_hash, error",
                        [
                         (None, pytest.raises(PermissionDenied)),
                         ("This is Dummy", pytest.raises(PermissionDenied)),
                         ("6b68b8e2dd2a6bec300ef91572270723", does_not_raise())
                        ])
def test_reset_edgepi_memory(mocker, bin_hash, error, eeprom):
    mocker.patch(
        "edgepi.eeprom.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__write_edgepi_reserved_memory")
    with error:
        eeprom.reset_edgepi_memory(bin_hash, base64.b64decode(DEFAULT_EEPROM_BIN_B64))

def test_check_default_bin():
    default_bin_file = read_binfile()
    default_bin = base64.b64decode(DEFAULT_EEPROM_BIN_B64)
    assert default_bin_file == default_bin
