'''unit test for access eeprom'''

# pylint: disable=C0413
# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372

from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))
import sys
sys.modules['periphery'] = mock.MagicMock()

from contextlib import nullcontext as does_not_raise
import json
import pytest

from edgepi.utilities.crc_8_atm import CRC_BYTE_SIZE, check_crc, get_crc
from edgepi.calibration.eeprom_constants import MessageFieldNumber, EdgePiMemoryInfo, EEPROMInfo
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM, MemoryOutOfBound
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout

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
    with open(PATH+"/serializedFile","rb") as fd:
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
    read_result = eeprom._EdgePiEEPROM__sequential_read( reg_addr, length)
    assert read_result == result

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
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
                return_value =data)
    # pylint: disable=protected-access
    length = eeprom._EdgePiEEPROM__allocated_memory(EdgePiMemoryInfo.USED_SPACE.value)
    assert length == result

def test__read_edgepi_reserved_memory(mocker, eeprom):
    data_b = read_binfile()
    # pylint: disable=protected-access
    data_l = eeprom._EdgePiEEPROM__generate_data_list(data_b)
    # pylint: disable=protected-access
    pages = eeprom._EdgePiEEPROM__generate_list_of_pages_crc(data_l)

    # pylint: disable=protected-access
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__allocated_memory",
                 return_value = (data_l[0]<<8) + data_l[1])
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
                side_effect = list(pages))
    # pylint: disable=protected-access
    byte_string = eeprom._EdgePiEEPROM__read_edgepi_reserved_memory()
    assert byte_string == data_b

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


KEYS = '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAnwu+S/OI3Hl0BCNQASv0HU5Jc4KUT2X4/tLykG+TmZ\
Qcd6pE\nv7fji6ZoW/dl8dKwwdi/cfSS/J5Iv+5FwQU4KGNBbhVAnmJeLd+PMUT4bQTf9rVF\nHsDoIPoQLDH7jmBu8ai7jQ0hY\
5SqPbynPGELFrk/vEpHwg/8fO4lbw1YxwgGc0SR\n8k1tFdi4On7NymBiv88HOsrrziAPGCd7Hc07s+SdFQF+nDPidyM1pMqvUC\
25c5Sk\ncsrBlMgmcSRY8y6MJFPObg0ahLsI/YT+jT2G6AioQOz9ZJ89DSzjEfoFK9KlIzq1\n46THPR8Tdc9quchsqfX1zvxKd\
rQPbdtC7ZnMhQIDAQABAoIBAQCccv3PUpGXZzVz\neJUTgfwQ89iW8qUXcVS8vh7za35CvYo/QFN+T9JapefUR4mVlk5fcOnpm8\
8XBlDD\n1AvzskGqoPBU7DzzUAoaj+YYbiL9gqUY1vlWJiZxgep0vvoX9M5Nk1BikL7+aNgK\nANB1OXSh9ro2as8pm3YgIlbaZ\
cOli7doqtDM4kzxpKOhSAwtQqAS15GwMsKyhs1q\nvN6BqTBQE7XjdO5k1GCT4+vWEnptKMlLxi/zj1uAXuAmujKHf3FcNqnrmN\
Q2v5+g\nNmuFCiknrtK5p5va67g6JgWqy45EG5CJLupIpM31xmewFXtlsfh3/fYSzkZqK9jX\nHg/Wq7ShAoGBAMqzZTr2kjxtP\
0UjN4S5L0da7k4UX+4GEJRrQgG6RUgrL5eq4tfc\nT4DU7mp7SAb7FVwZmJ5kXZ33aQBF6UYRuIpzUWRT+QOfzeTeJSQGAR8Ng/\
STNaUt\nD9XalRJSYn49LMGTgFebKJakIUC7lZ0ZZxpP1yFZbmYtJN1xFB/jhfGdAoGBAMjd\nwuzc5VPJV5fQte6lTcnTzkqnP\
XnSvpf4sK+22i/1xGi0kbdimQiXHPj2xnwQmygN\n3a+l2ysChimOx2qqVdeFQbAveKwYYSk41R10PmsQE14CgREN3r1XcXGz4m\
qXpL8l\n7Ry2HOIDQjTRVye2YdRO0zu3+egdFz4UTnxE8yYJAoGBAIM5+MNfdfTg1SExV3P5\nX35WhAjQb/psurcbaTQtH0VFk\
B4kZ49P9bh2IZOWFF9Qldd2SrPgTitCTRv8JrVS\nK6KWXY8SPhf2kRkmJ+1WZctwuIjR9Nzme2X7iJ6/7zvC5wK7N0+AB5rezx\
hVWNrH\n41PJdIEGoM5NU5x45IpwhfqRAoGANpYdbOUy5SwoQ7eSWYJOu3R18U+1oy+kYART\nb80PSk1NzO6VUvLWh8EZPIdDt\
V+F6sKp5hv6jZun/g8xHkmf/mvWSBz+fDY74Uny\nkIiQlePOf5PKo2nTiD0FNVMfSrxfJxsVbuIGw10DVvs05jPoLhwlx2rd3T\
haoqI+\nGgNa2JECgYEAwEEEq7dxGXYmlIhTs5IiEleLjBydQ9B1P8zIIApLJdHuu50K7ifq\nVYWC0QMrAr4lWmJ3ZAmewtrgD\
h4/6JBWKdpKfX6qm88MpID0arS+jJkQBuMNIafI\nGqnLR1sn5N91UjPItE3NPhYX5LvQMjIuHt8AiyNepTxS32VzVTx2z+A=\n\
-----END RSA PRIVATE KEY-----\n'

def test_get_edgepi_reserved_data(mocker, eeprom):
    # pylint: disable=protected-access
    mocker.patch(
        "edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__read_edgepi_reserved_memory",
        return_value = read_binfile())
    memory_contents = EepromLayout()
    memory_contents.ParseFromString(read_binfile())
    eeprom_data = eeprom.get_edgepi_reserved_data()
    for key, value in eeprom_data.dac_calib_params.items():
        assert value.gain == pytest.approx(dac_dict_calib[key].gain)
        assert value.offset == pytest.approx(dac_dict_calib[key].offset)
    for key, value in eeprom_data.adc_calib_params.items():
        assert value.gain == pytest.approx(adc_dict_calib[key].gain)
        assert value.offset == pytest.approx(adc_dict_calib[key].offset)
    for key, value in eeprom_data.tc_calib_params.items():
        assert value.gain == pytest.approx(tc_dict_calib[key].gain)
        assert value.offset == pytest.approx(tc_dict_calib[key].offset)
    for key, value in eeprom_data.tc_hw_params.items():
        assert value == pytest.approx(tc_dict_hw[key])
    for key, value in eeprom_data.rtd_calib_params.items():
        assert value.gain == pytest.approx(rtd_dict_calib[key].gain)
        assert value.offset == pytest.approx(rtd_dict_calib[key].offset)
    for key, value in eeprom_data.rtd_hw_params.items():
        assert value == pytest.approx(rtd_dict_hw[key])
    assert eeprom_data.serial == '20221110-021'
    assert eeprom_data.model == 'EdgePi-Bearbone'
    assert eeprom_data.client_id_config == 'client-id__shadow'
    assert eeprom_data.client_id_data == 'client-id'
    assert eeprom_data.thing_id == 'thing-id'
    assert eeprom_data.config_key.certificate == KEYS
    assert eeprom_data.config_key.private == KEYS
    assert eeprom_data.data_key.certificate == KEYS
    assert eeprom_data.data_key.certificate == KEYS

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
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__page_write_register")
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

def test_read_memory(mocker, eeprom):
    dummy_data = read_dummy_json("dummy_0.json")
    dummy_data_b = bytes(json.dumps(dummy_data), "utf-8")
    # pylint: disable=protected-access
    dummy_data_l = eeprom._EdgePiEEPROM__generate_data_list(dummy_data_b)
    # pylint: disable=protected-access
    pages = eeprom._EdgePiEEPROM__generate_list_of_pages_crc(dummy_data_l)
    mocker.patch(
        "edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
        side_effect = pages)
    data_size = (dummy_data_l[0]<<8) + dummy_data_l[1]
    result = eeprom.read_memory(data_size)
    assert result == list(dummy_data_b)

@pytest.mark.parametrize("mem_size, dummy_size, result, error",
                        [(3, 3,[False, False], does_not_raise()),
                         (512, 512, [False, False], does_not_raise()),
                         (0x3FFF, 0, [True, False], pytest.raises(ValueError)),
                         (0x3FFC, 5460, [True, False], does_not_raise()),
                         (0xFFFF, 0, [False, True], does_not_raise()),
                        ])
def test_init_memory(mocker, mem_size, dummy_size, result, error, eeprom):
    mocker.patch(
        "edgepi.calibration.edgepi_eeprom.EdgePiEEPROM.read_memory",
        return_value = list(bytes(json.dumps([2]*dummy_size), "utf8")))
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__allocated_memory",
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
