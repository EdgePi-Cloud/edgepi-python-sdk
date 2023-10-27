'''unit test for access eeprom'''
# pylint: disable=C0413
# pylint: disable=no-member
# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372
from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.calibration.protobuf_mapping import EdgePiEEPROMData
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/serializedFile","rb") as fd:
        b_string = fd.read()
    return b_string

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

def test_edgepi_eeprom_data():
    memory_map = EepromLayout()
    memory_map.ParseFromString(read_binfile())
    eeprom_data = EdgePiEEPROMData(memory_map)
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
