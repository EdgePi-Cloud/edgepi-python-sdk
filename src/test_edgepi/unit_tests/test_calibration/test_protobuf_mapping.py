'''unit test for access eeprom'''
# pylint: disable=C0413
# pylint: disable=no-member
from unittest import mock
import os
PATH = os.path.dirname(os.path.abspath(__file__))
import sys
sys.modules['periphery'] = mock.MagicMock()

from edgepi.calibration.protobuf_mapping import EdgePiEEPROMData, Keys
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/serializedFile","rb") as fd:
        b_string = fd.read()
    return b_string

dict_calib = {0:CalibParam(gain = 1.0189533233642578, offset=-0.01578296162188053),
             1:CalibParam(gain = 1.0225214958190918, offset=-0.017427191138267517),
             2:CalibParam(gain = 1.023260474205017, offset=-0.018893923610448837),
             3:CalibParam(gain = 1.019696831703186, offset=-0.015452692285180092),
             4:CalibParam(gain = 1.0220204591751099, offset=-0.017059000208973885),
             5:CalibParam(gain = 1.020483374595642, offset=-0.016757730394601822),
             6:CalibParam(gain = 1.0185232162475586, offset=-0.014892885461449623),
             7:CalibParam(gain = 1.019013524055481, offset=-0.014892730861902237)}

keys = '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAnwu+S/OI3Hl0BCNQASv0HU5Jc4KUT2X4/tLykG+TmZ\
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
    assert eeprom_data.dac_calib_parms == dict_calib
    assert eeprom_data.adc_calib_parms == dict_calib
    assert eeprom_data.tc_calib_parms == dict_calib
    assert eeprom_data.rtd_calib_parms == dict_calib
    assert eeprom_data.serial == '20221110-021'
    assert eeprom_data.model == 'EdgePi-Bearbone'
    assert eeprom_data.client_id == 'SO-2022-1023'
    assert eeprom_data.config_key.certificate == keys
    assert eeprom_data.config_key.private == keys
    assert eeprom_data.data_key.certificate == keys
    assert eeprom_data.data_key.certificate == keys
