'''integration test for access eeprom'''

# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position
# https://github.com/protocolbuffers/protobuf/issues/10372
# TODO: I2C Transaction fails without 0.002ms delay

import os
PATH = os.path.dirname(os.path.abspath(__file__))
import string
import random

import time
import logging
import pytest
_logger = logging.getLogger(__name__)

from edgepi.calibration.eeprom_constants import EdgePiMemoryInfo
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM
from edgepi.calibration.eeprom_constants import MessageFieldNumber

@pytest.fixture(name="eeprom")
def fixture_test_eeprom():
    eeprom = EdgePiEEPROM()
    return eeprom

@pytest.mark.parametrize("data, address",
                        [
                         (list(range(0,64)),0),
                         (list(range(64,128)),64),
                        ])
# pylint: disable=protected-access
def test__page_write_register(data, address, eeprom):
    addrx = EdgePiMemoryInfo.USER_SPACE_START_BYTE.value + address
    initial_data = eeprom._EdgePiEEPROM__sequential_read(addrx,len(data))
    eeprom._EdgePiEEPROM__page_write_register(addrx, data)
    time.sleep(0.5)
    new_data = eeprom._EdgePiEEPROM__sequential_read(addrx,len(data))
    time.sleep(0.5)
    eeprom._EdgePiEEPROM__page_write_register(addrx, [255]*len(data))
    _logger.info(f"data to write = {data}")
    _logger.info(f"initial data  = {initial_data}")
    _logger.info(f"new data      = {new_data}")
    for indx, init_data in enumerate(initial_data):
        assert init_data != new_data[indx]
        assert new_data[indx] == data[indx]

DUMMY_KEY = '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAnwu+S/OI3Hl0BCNQASv0HU5Jc4KUT2X4/tLyk\
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
h4/6JBWKdpKfX6qm88MpID0arS+jJkQBuMNIafI\nGqnLR1sn5N91UjPItE3NPhYX5LvQMjIuHt8AiyNepTxS32VzVTx2z+A=G+\
TmZ\n-----END RSA PRIVATE KEY-----\n'

def test_set_edgepi_reserved_data(eeprom):
    original_data = eeprom.get_edgepi_reserved_data()

    for _ in range(10):
        # initializing size of string
        str_len = 100
        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=str_len))

        # Modified data to write to memory
        modified_data = eeprom.get_edgepi_reserved_data()
        modified_data.config_key.certificate = DUMMY_KEY + res
        modified_data.config_key.private = DUMMY_KEY + res
        modified_data.data_key.certificate = DUMMY_KEY + res
        modified_data.data_key.private = DUMMY_KEY + res
        # Write modified data
        eeprom.set_edgepi_reserved_data(modified_data, MessageFieldNumber.ALL)
        modified_data = eeprom.get_edgepi_reserved_data()

        assert modified_data.dac_calib_params == original_data.dac_calib_params
        assert modified_data.adc_calib_params == original_data.adc_calib_params
        assert modified_data.rtd_calib_params == original_data.rtd_calib_params
        assert modified_data.rtd_hw_params == original_data.rtd_hw_params
        assert modified_data.tc_calib_params == original_data.tc_calib_params
        assert modified_data.tc_hw_params == original_data.tc_hw_params
        assert modified_data.config_key != original_data.config_key
        assert modified_data.data_key != original_data.data_key
        assert modified_data.serial == original_data.serial
        assert modified_data.model == original_data.model
        assert modified_data.client_id_config == original_data.client_id_config
        assert modified_data.client_id_data == original_data.client_id_data
        assert modified_data.thing_id == original_data.thing_id

    # Write the original data back
    eeprom.set_edgepi_reserved_data(original_data, MessageFieldNumber.ALL)
