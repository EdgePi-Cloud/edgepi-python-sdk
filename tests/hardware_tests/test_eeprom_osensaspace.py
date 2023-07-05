'''hardware test for eeprom user space'''

# pylint: disable=no-name-in-module
# pylint: disable=wrong-import-position
# https://github.com/protocolbuffers/protobuf/issues/10372

import logging
_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import time
import os
PATH = os.path.dirname(os.path.abspath(__file__))

import pytest
from edgepi.eeprom.edgepi_eeprom import EdgePiEEPROM

@pytest.fixture(name="eeprom")
def fixture_test_dac():
    eeprom = EdgePiEEPROM()
    return eeprom

# Change ADC DAC Module Param
def test_osensa_space_modify_1(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.get_edgepi_data()
    time.sleep(0.5)
    eeprom_data_modify = eeprom.get_edgepi_data()
    time.sleep(0.5)

    for ch, calibs in eeprom_data_modify.dac_calib_params.items():
        calibs.gain = ch
        calibs.offset = ch

    for ch, calibs in eeprom_data_modify.adc_calib_params.items():
        calibs.gain = ch
        calibs.offset = ch

    eeprom.set_edgepi_data(eeprom_data_modify)
    time.sleep(0.5)
    eeprom.set_edgepis_data(eeprom_data_modify)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.get_edgepi_data()
    assert eeprom_data_origin.dac_calib_params != eeprom_data_modify.dac_calib_params
    assert eeprom_data_origin.adc_calib_params != eeprom_data_modify.adc_calib_params

# TC and RTD modification
def test_osensa_space_modify_2(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.get_edgepi_data()
    time.sleep(5)
    eeprom_data_modify = eeprom.get_edgepi_data()
    time.sleep(5)

    for ch, calibs in eeprom_data_modify.rtd_calib_params.items():
        calibs.gain = ch
        calibs.offset = ch
    for ch, _ in eeprom_data_modify.rtd_hw_params.items():
        eeprom_data_modify.rtd_hw_params[ch] = 1818.5
    for ch, calibs in eeprom_data_modify.tc_calib_params.items():
        calibs.gain = ch
        calibs.offset = ch
    for ch, _ in eeprom_data_modify.tc_hw_params.items():
        eeprom_data_modify.tc_hw_params[ch] = 1818.5

    eeprom.set_edgepi_data(eeprom_data_modify)
    time.sleep(0.5)
    eeprom.set_edgepi_data(eeprom_data_modify)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.get_edgepi_data()
    assert eeprom_data_origin.rtd_calib_params != eeprom_data_modify.rtd_calib_params
    assert eeprom_data_origin.tc_calib_params != eeprom_data_modify.tc_calib_params
    assert eeprom_data_origin.rtd_hw_params != eeprom_data_modify.rtd_hw_params
    assert eeprom_data_origin.tc_hw_params != eeprom_data_modify.tc_hw_params

def test_osensa_space_modify_3(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.get_edgepi_data()
    time.sleep(0.5)
    eeprom_data_modify = eeprom.get_edgepi_data()
    time.sleep(0.5)

    eeprom_data_modify.config_key.certificate = "This is config certificate"
    eeprom_data_modify.config_key.private = "This is config private"
    eeprom_data_modify.data_key.certificate = "This is data certificate"
    eeprom_data_modify.data_key.private = "This is data private"

    eeprom.set_edgepi_data(eeprom_data_modify)
    time.sleep(0.5)
    eeprom.set_edgepi_data(eeprom_data_modify)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.get_edgepi_data()
    assert eeprom_data_origin.config_key != eeprom_data_modify.config_key
    assert eeprom_data_origin.data_key != eeprom_data_modify.data_key
