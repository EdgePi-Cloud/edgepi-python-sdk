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
    assert eeprom_data.client_id_config == 'client-id__shadow'
    assert eeprom_data.client_id_data == 'client-id'
    assert eeprom_data.thing_id == 'thing-id'
    assert eeprom_data.config_key.certificate == KEYS
    assert eeprom_data.config_key.private == KEYS
    assert eeprom_data.data_key.certificate == KEYS
    assert eeprom_data.data_key.certificate == KEYS

def test_edgepi_protobuf_pack_data():
    original_memory_map = EepromLayout()
    changed_memory_map = EepromLayout()
    original_memory_map.ParseFromString(read_binfile())
    changed_memory_map.ParseFromString(read_binfile())
    change_data = EdgePiEEPROMData(changed_memory_map)
    for value in change_data.dac_calib_params.values():
        value.gain = 1
        value.offset = 2
    for value in change_data.adc_calib_params.values():
        value.gain = 1
        value.offset = 2
    for value in change_data.rtd_calib_params.values():
        value.gain = 1
        value.offset = 2
    for value in change_data.tc_calib_params.values():
        value.gain = 1
        value.offset = 2
    for key, value in change_data.rtd_hw_params.items():
        change_data.rtd_hw_params[key] = 1
    for key, value in change_data.tc_hw_params.items():
        change_data.tc_hw_params[key] = 1
    change_data.config_key.certificate = "config_certificate"
    change_data.config_key.private = "config_private"
    change_data.data_key.certificate = "data_certificate"
    change_data.data_key.private = "data_private"
    change_data.client_id_config = "This is new client id config"
    change_data.client_id_data = "This is new client id data"
    change_data.thing_id = "This is new thing id"
    change_data.model = "This is new model"
    change_data.serial = "this is new serial number"
    change_data.pack_dataclass(changed_memory_map)
    assert original_memory_map != changed_memory_map
