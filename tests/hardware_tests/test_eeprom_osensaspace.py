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
from edgepi.calibration.eeprom_constants import MessageFieldNumber
from edgepi.calibration.edgepi_eeprom import EdgePiEEPROM
from edgepi.calibration.protobuf_mapping import EdgePiEEPROMData

@pytest.fixture(name="eeprom")
def fixture_test_dac():
    eeprom = EdgePiEEPROM()
    return eeprom

def read_binfile():
    """Read the dummy serializedFile and return byte string"""
    with open(PATH+"/serializedFile","rb") as fd:
        b_string = fd.read()
    return b_string

# Reserved space write/read test
def  test_set_edgepi_reserved_data(eeprom):
    _logger.info("Writing dummy serialized binary to the Osensa Reserved Space")
    eeprom.eeprom_layout.ParseFromString(read_binfile())
    eeprom_data_w = EdgePiEEPROMData(eeprom.eeprom_layout)
    time.sleep(5)
    eeprom.set_edgepi_reserved_data(eeprom_data_w, MessageFieldNumber.ALL)
    time.sleep(5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_r = eeprom.get_edgepi_reserved_data()
    assert eeprom_data_w.adc_calib_params == eeprom_data_r.adc_calib_params
    assert eeprom_data_w.dac_calib_params == eeprom_data_r.dac_calib_params
    assert eeprom_data_w.rtd_calib_params == eeprom_data_r.rtd_calib_params
    assert eeprom_data_w.rtd_hw_params == eeprom_data_r.rtd_hw_params
    assert eeprom_data_w.tc_calib_params == eeprom_data_r.tc_calib_params
    assert eeprom_data_w.tc_hw_params == eeprom_data_r.tc_hw_params
    assert eeprom_data_w.config_key == eeprom_data_r.config_key
    assert eeprom_data_w.data_key == eeprom_data_r.data_key
    assert eeprom_data_w.model == eeprom_data_r.model
    assert eeprom_data_w.serial == eeprom_data_r.serial
    assert eeprom_data_w.client_id == eeprom_data_r.client_id

# Change ADC DAC Module Param
def test_osensa_space_modify_1(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.get_edgepi_reserved_data()
    time.sleep(0.5)
    eeprom_data_modify = eeprom.get_edgepi_reserved_data()
    time.sleep(0.5)

    for ch, calibs in eeprom_data_modify.dac_calib_params.items():
        calibs.gain = ch
        calibs.offset = ch

    for ch, calibs in eeprom_data_modify.adc_calib_params.items():
        calibs.gain = ch
        calibs.offset = ch

    eeprom.set_edgepi_reserved_data(eeprom_data_modify, MessageFieldNumber.DAC)
    time.sleep(0.5)
    eeprom.set_edgepi_reserved_data(eeprom_data_modify, MessageFieldNumber.ADC)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.get_edgepi_reserved_data()
    assert eeprom_data_origin.dac_calib_params != eeprom_data_modify.dac_calib_params
    assert eeprom_data_origin.adc_calib_params != eeprom_data_modify.adc_calib_params

# TC and RTD modification
def test_osensa_space_modify_2(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.get_edgepi_reserved_data()
    time.sleep(5)
    eeprom_data_modify = eeprom.get_edgepi_reserved_data()
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

    eeprom.set_edgepi_reserved_data(eeprom_data_modify, MessageFieldNumber.RTD)
    time.sleep(0.5)
    eeprom.set_edgepi_reserved_data(eeprom_data_modify, MessageFieldNumber.TC)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.get_edgepi_reserved_data()
    assert eeprom_data_origin.rtd_calib_params != eeprom_data_modify.rtd_calib_params
    assert eeprom_data_origin.tc_calib_params != eeprom_data_modify.tc_calib_params
    assert eeprom_data_origin.rtd_hw_params != eeprom_data_modify.rtd_hw_params
    assert eeprom_data_origin.tc_hw_params != eeprom_data_modify.tc_hw_params

def test_osensa_space_modify_3(eeprom):
    _logger.info("Modifying Module Params")
    eeprom_data_origin = eeprom.get_edgepi_reserved_data()
    time.sleep(0.5)
    eeprom_data_modify = eeprom.get_edgepi_reserved_data()
    time.sleep(0.5)

    eeprom_data_modify.config_key.certificate = "This is config certificate"
    eeprom_data_modify.config_key.private = "This is config private"
    eeprom_data_modify.data_key.certificate = "This is data certificate"
    eeprom_data_modify.data_key.private = "This is data private"

    eeprom.set_edgepi_reserved_data(eeprom_data_modify, MessageFieldNumber.CONFIGS_KEY)
    time.sleep(0.5)
    eeprom.set_edgepi_reserved_data(eeprom_data_modify, MessageFieldNumber.DATA_KEY)
    time.sleep(0.5)

    _logger.info("Reading Osensa Reserved Space")
    eeprom_data_modify = eeprom.get_edgepi_reserved_data()
    assert eeprom_data_origin.config_key != eeprom_data_modify.config_key
    assert eeprom_data_origin.data_key != eeprom_data_modify.data_key