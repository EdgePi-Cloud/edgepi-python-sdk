'''unit test for edgepi_calibration'''

# pylint: disable=C0413


from errno import EDEADLK
from modulefinder import Module
from unittest import mock
import sys
sys.modules['periphery'] = mock.MagicMock()

import pytest
from edgepi.calibration.edgepi_calibration import EdgePiCalibration
from edgepi.calibration.eeprom_constants import ModuleNames
from edgepi.calibration.calibration_constants import (
    NumOfCh,
    CalibParam,
    ReferenceV
)

# @pytest.fixture(name="calib")
# def fixture_test_dac():
#     yield EdgePiCalibration()

@pytest.mark.parametrize("module_name, result", [(ModuleNames.DAC, [0, 8]),
                                                 (ModuleNames.ADC, [1, 8]),
                                                 (ModuleNames.RTD, [2, 1]),
                                                 (ModuleNames.TC, [3, 1])])
def test_init_EdgePiCalibration(module_name, result):
    edge_calib = EdgePiCalibration(module_name)
    assert edge_calib.module == result[0]
    assert edge_calib.num_of_ch == result[1]

@pytest.mark.parametrize("module_name, result", [(ModuleNames.DAC, [1, 0]),
                                                 (ModuleNames.ADC, [1, 0]),
                                                 (ModuleNames.RTD, [1, 0]),
                                                 (ModuleNames.TC, [1, 0])])
def test_generate_calib_param_dict(module_name, result):
    edge_calib = EdgePiCalibration(module_name)
    calib_dict = edge_calib._EdgePiCalibration__generate_calib_param_dict()
    for _, value in calib_dict.items():
        assert value.gain == result[0]
        assert value.offset == result[1]
    dict_length = len(calib_dict.values())
    assert dict_length == edge_calib.num_of_ch

@pytest.mark.parametrize("module_name, num_of_points, result", [(ModuleNames.DAC, 10, 0),
                                                                (ModuleNames.ADC, 5, 0),
                                                                (ModuleNames.RTD, 2, 0),
                                                                (ModuleNames.TC,  7, 0)])
def test_generate_measurements_dict(module_name, num_of_points, result):
    edge_calib = EdgePiCalibration(module_name)
    measurements_dict = edge_calib._EdgePiCalibration__generate_measurements_dict(num_of_points)
    for _, value in measurements_dict.items():
        assert value['expected'] == result
        assert value['actual'] == result
    dict_length = len(measurements_dict.keys())
    assert dict_length == num_of_points