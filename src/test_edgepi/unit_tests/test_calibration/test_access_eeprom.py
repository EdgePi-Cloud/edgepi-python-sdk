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

from edgepi.calibration.eeprom_constants import MessageFieldNumber, EdgePiMemoryInfo
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

@pytest.mark.parametrize("reg_addr, mock_val, result", [(1, [23], [23])])
def test_selective_read(mocker, eeprom, reg_addr, mock_val, result):
    mocker.patch("edgepi.peripherals.i2c.I2CDevice.transfer",return_value = mock_val)
    # pylint: disable=protected-access
    read_result = eeprom._EdgePiEEPROM__selective_read(reg_addr)
    assert read_result == result



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
    # pylint: disable=protected-access
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
                return_value =mock_value)
    # pylint: disable=protected-access
    length = eeprom._EdgePiEEPROM__allocated_memory(EdgePiMemoryInfo.USED_SPACE.value)
    assert length == result

def test__read_edgepi_reserved_memory(mocker, eeprom):
    # pylint: disable=protected-access
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__allocated_memory")
    mocker.patch("edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
                return_value =list(read_binfile()))
    # pylint: disable=protected-access
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


dac_dict_calib = {0:CalibParam(gain = 1.02383653, offset=-0.0164757),
                  1:CalibParam(gain = 1.02283154, offset=-0.018963),
                  2:CalibParam(gain = 1.02610898, offset=-0.0153855),
                  3:CalibParam(gain = 1.02465811, offset=-0.0182012),
                  4:CalibParam(gain = 1.02623188, offset=-0.0179865),
                  5:CalibParam(gain = 1.02696733, offset=-0.0169919),
                  6:CalibParam(gain = 1.0248366, offset=-0.0195936),
                  7:CalibParam(gain = 1.02198715, offset=-0.0179717)}

adc_dict_calib = {0:CalibParam(gain = 0.998441907, offset=0.035948182),
                  1:CalibParam(gain = 0.998551392, offset=0.03190953),
                  2:CalibParam(gain = 1.004123580, offset=-0.039846713),
                  3:CalibParam(gain = 0.996197528, offset=0.05191299),
                  4:CalibParam(gain = 1.000529260, offset=0.00375247),
                  5:CalibParam(gain = 0.995760365, offset=0.05806301),
                  6:CalibParam(gain = 0.993060022, offset=0.09193925),
                  7:CalibParam(gain = 0.997010247, offset=0.04080028),
                  8:CalibParam(gain = 0.998583581, offset=-0.004391864),
                  9:CalibParam(gain = 0.996344494, offset=0.09228059),
                  10:CalibParam(gain = 0.995856966, offset=0.05618589),
                  11:CalibParam(gain = 0.997157199, offset=-0.049672102)}

rtd_dict_calib = {0:CalibParam(gain = 1, offset=0)}
rtd_dict_hw= {0:1985.60}
tc_dict_calib = {0:CalibParam(gain = 1.024272873, offset=-0.018334615)}
tc_dict_hw = {0:1}


KEYS = '-----BEGIN RSA PRIVATE KEY-----\r\nMIIEpQIBAAKCAQEAnwu+S/OI3Hl0BCNQASv0HU5Jc4KUT2X4/tLykG+T\
mZQcd6pE\r\nv7fji6ZoW/dl8dKwwdi/cfSS/J5Iv+5FwQU4KGNBbhVAnmJeLd+PMUT4bQTf9rVF\r\nHsDoIPoQLDH7jmBu8ai\
7jQ0hY5SqPbynPGELFrk/vEpHwg/8fO4lbw1YxwgGc0SR\r\n8k1tFdi4On7NymBiv88HOsrrziAPGCd7Hc07s+SdFQF+nDPidy\
M1pMqvUC25c5Sk\r\ncsrBlMgmcSRY8y6MJFPObg0ahLsI/YT+jT2G6AioQOz9ZJ89DSzjEfoFK9KlIzq1\r\n46THPR8Tdc9qu\
chsqfX1zvxKdrQPbdtC7ZnMhQIDAQABAoIBAQCccv3PUpGXZzVz\r\neJUTgfwQ89iW8qUXcVS8vh7za35CvYo/QFN+T9JapefU\
R4mVlk5fcOnpm88XBlDD\r\n1AvzskGqoPBU7DzzUAoaj+YYbiL9gqUY1vlWJiZxgep0vvoX9M5Nk1BikL7+aNgK\r\nANB1OXS\
h9ro2as8pm3YgIlbaZcOli7doqtDM4kzxpKOhSAwtQqAS15GwMsKyhs1q\r\nvN6BqTBQE7XjdO5k1GCT4+vWEnptKMlLxi/zj1\
uAXuAmujKHf3FcNqnrmNQ2v5+g\r\nNmuFCiknrtK5p5va67g6JgWqy45EG5CJLupIpM31xmewFXtlsfh3/fYSzkZqK9jX\r\nH\
g/Wq7ShAoGBAMqzZTr2kjxtP0UjN4S5L0da7k4UX+4GEJRrQgG6RUgrL5eq4tfc\r\nT4DU7mp7SAb7FVwZmJ5kXZ33aQBF6UYR\
uIpzUWRT+QOfzeTeJSQGAR8Ng/STNaUt\r\nD9XalRJSYn49LMGTgFebKJakIUC7lZ0ZZxpP1yFZbmYtJN1xFB/jhfGdAoGBAMj\
d\r\nwuzc5VPJV5fQte6lTcnTzkqnPXnSvpf4sK+22i/1xGi0kbdimQiXHPj2xnwQmygN\r\n3a+l2ysChimOx2qqVdeFQbAveK\
wYYSk41R10PmsQE14CgREN3r1XcXGz4mqXpL8l\r\n7Ry2HOIDQjTRVye2YdRO0zu3+egdFz4UTnxE8yYJAoGBAIM5+MNfdfTg1\
SExV3P5\r\nX35WhAjQb/psurcbaTQtH0VFkB4kZ49P9bh2IZOWFF9Qldd2SrPgTitCTRv8JrVS\r\nK6KWXY8SPhf2kRkmJ+1W\
ZctwuIjR9Nzme2X7iJ6/7zvC5wK7N0+AB5rezxhVWNrH\r\n41PJdIEGoM5NU5x45IpwhfqRAoGANpYdbOUy5SwoQ7eSWYJOu3R\
18U+1oy+kYART\r\nb80PSk1NzO6VUvLWh8EZPIdDtV+F6sKp5hv6jZun/g8xHkmf/mvWSBz+fDY74Uny\r\nkIiQlePOf5PKo2\
nTiD0FNVMfSrxfJxsVbuIGw10DVvs05jPoLhwlx2rd3ThaoqI+\r\nGgNa2JECgYEAwEEEq7dxGXYmlIhTs5IiEleLjBydQ9B1P\
8zIIApLJdHuu50K7ifq\r\nVYWC0QMrAr4lWmJ3ZAmewtrgDh4/6JBWKdpKfX6qm88MpID0arS+jJkQBuMNIafI\r\nGqnLR1sn\
5N91UjPItE3NPhYX5LvQMjIuHt8AiyNepTxS32VzVTx2z+A=\r\n-----END RSA PRIVATE KEY-----\r\n'

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
    assert eeprom_data.client_id == 'SO-2022-1023'
    assert eeprom_data.config_key.certificate == KEYS
    assert eeprom_data.config_key.private == KEYS
    assert eeprom_data.data_key.certificate == KEYS
    assert eeprom_data.data_key.certificate == KEYS

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

@pytest.mark.parametrize("mem_address,data,expected",
                        [(0, [1,2,3,4,5,6], [[1,2,3,4,5,6]]),
                         (60, [60,61,62,63], [[60,61,62,63]]),
                         (60, [60,61,62,63,64], [[60,61,62,63],[64]]),
                         (63, [63,64,65,66,67,68],[[63],[64,65,66,67,68]]),
                         (63, [63, 64, 65, 66, 67,
                               68, 69, 70, 71, 72,
                               73, 74, 75, 76, 77,
                               78, 79, 80, 81, 82,
                               83, 84, 85, 86, 87,
                               88, 89, 90, 91, 92,
                               93, 94, 95, 96, 97,
                               98, 99, 100, 101, 102,
                               103, 104, 105, 106, 107,
                               108, 109, 110, 111, 112,
                               113, 114, 115, 116, 117,
                               118, 119, 120, 121, 122,
                               123, 124, 125, 126],[[63], [64, 65, 66, 67,
                                                           68, 69, 70, 71, 72,
                                                           73, 74, 75, 76, 77,
                                                           78, 79, 80, 81, 82,
                                                           83, 84, 85, 86, 87,
                                                           88, 89, 90, 91, 92,
                                                           93, 94, 95, 96, 97,
                                                           98, 99, 100, 101, 102,
                                                           103, 104, 105, 106, 107,
                                                           108, 109, 110, 111, 112,
                                                           113, 114, 115, 116, 117,
                                                           118, 119, 120, 121, 122,
                                                           123, 124, 125, 126]]),
                         (63, [63, 64, 65, 66, 67,
                               68, 69, 70, 71, 72,
                               73, 74, 75, 76, 77,
                               78, 79, 80, 81, 82,
                               83, 84, 85, 86, 87,
                               88, 89, 90, 91, 92,
                               93, 94, 95, 96, 97,
                               98, 99, 100, 101, 102,
                               103, 104, 105, 106, 107,
                               108, 109, 110, 111, 112,
                               113, 114, 115, 116, 117,
                               118, 119, 120, 121, 122,
                               123, 124, 125, 126, 127, 128],[[63],
                                                              [64, 65, 66, 67,
                                                               68, 69, 70, 71, 72,
                                                               73, 74, 75, 76, 77,
                                                               78, 79, 80, 81, 82,
                                                               83, 84, 85, 86, 87,
                                                               88, 89, 90, 91, 92,
                                                               93, 94, 95, 96, 97,
                                                               98, 99, 100, 101, 102,
                                                               103, 104, 105, 106, 107,
                                                               108, 109, 110, 111, 112,
                                                               113, 114, 115, 116, 117,
                                                               118, 119, 120, 121, 122,
                                                               123, 124, 125, 126, 127],
                                                              [128]])
                        ])
def test__generate_list_of_pages(mem_address, data, expected, eeprom):
    # pylint: disable=protected-access
    result = eeprom._EdgePiEEPROM__generate_list_of_pages(mem_address, data)
    assert result == expected

@pytest.mark.parametrize("mem_address",
                        [(EdgePiMemoryInfo.USER_SPACE_START_BYTE.value)])
def test__generate_list_of_pages_reset(mem_address, eeprom):
    # pylint: disable=protected-access
    # pylint: disable=line-too-long
    data = [255]*(EdgePiMemoryInfo.USER_SPACE_END_BYTE.value-EdgePiMemoryInfo.USER_SPACE_START_BYTE.value+1)
    page_n = eeprom._EdgePiEEPROM__generate_list_of_pages(mem_address, data)
    assert len(page_n) == len(data)/64

@pytest.mark.parametrize("mem_address,json_file_name",
                        [(0, "dummy_0.json"),
                         (2, "dummy_0.json"),
                         ])
def test__generate_list_of_pages_json(mem_address, json_file_name,eeprom):
    json_data = read_dummy_json(json_file_name)
    data_b = bytes(json.dumps(json_data,indent=0,sort_keys=False,separators=(',', ':')), "utf-8")
    data_l = list(data_b)
    # pylint: disable=protected-access
    page_n = eeprom._EdgePiEEPROM__generate_list_of_pages(mem_address, list(data_l))
    target = iter(data_l)
    for page in page_n:
        for val in page:
            assert val == next(target)


# TODO: add more teset cases
@pytest.mark.parametrize("mem_address, length, expected",
                        [(0, 34, list(range(0,34))),
                         (0, 64, list(range(0,64))),
                         (30, 34, list(range(30,(30+34)))),
                         (30, 35, list(range(30,(30+35)))),
                         (0, 128, list(range(0,(128)))),
                         (3, 128, list(range(3,(3+128))))
                        ])
def test_read_memory(mocker, mem_address, length, expected, eeprom):
    # pylint: disable=line-too-long
    # pylint: disable=protected-access
    dummay = eeprom._EdgePiEEPROM__generate_list_of_pages(mem_address, list(range(mem_address,mem_address+length)))
    mocker.patch(
        "edgepi.calibration.edgepi_eeprom.EdgePiEEPROM._EdgePiEEPROM__sequential_read",
        side_effect = dummay)
    result = eeprom.read_memory(mem_address, length)
    assert result == expected

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
