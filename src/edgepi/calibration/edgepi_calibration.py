'''
Module for generating calibration parameter data structure for each module. This module should be
able to generate new calibration parameters using measurements tools.
'''

from edgepi.eeprom.eeprom_constants import ModuleNames
from edgepi.calibration.calibration_constants import NumOfCh


class EdgePiCalibration():
    '''
    EdgePi Calibration Class handling the following functionality
    1. load calibration parameter
    2. store new calibration parameter
    3. calibration process for each module
        - Load measurement values
           - Edge Pi measurements
           - Equipment measurements
        - Calculation: use leat mean square method
    '''

    def __init__(self, module: ModuleNames):
        self.module = module.value
        self.num_of_ch = NumOfCh[module.name].value
        self.full_scale_range = None
        self.full_scale_code = None

    def generate_measurements_dict(self, num_of_points: int = None):
        '''
        Function to generate dictionary of measurements to generate calibration parameter. It will
        store expected and actual measurements at each data point for number_of_points length
        Args:
            num_of_points (int): number of points to be generated, used as length of the dictionary
        Return:
            measurements_dict (dict): dictionary mapping expected value to
            ie) {0 : {'input_unit' : int, 'expected_out' : float, 'actual_out' : float},
                 .
                 .
                 .
                 nth_point : {'input_unit' : int, 'expected_out' : float, 'actual_out' : float}}
        '''
        measurements_dict = {}
        for point in range(num_of_points):
            measurements_dict[point]= {'input_unit': 0 ,'expected_out': 0, 'actual_out': 0}
        return measurements_dict

    def generate_channel_measurements_dict(self, num_of_points: int = None):
        '''
        Function to generate measuremenst dictionary for each channel. This is neccessary to calibr-
        -ate each channel individually
        Args:
            num_of_points (int): number of points to be generated, used as length of the dictionary
        '''
        ch_measurements_dict = {}
        for ch in range(self.num_of_ch):
            ch_measurements_dict[ch] = self.generate_measurements_dict(num_of_points)
        return ch_measurements_dict

    def record_measurements(self, nth_measurements: dict = None,
                                  input_unit: int = None,
                                  expected: float = None,
                                  actual: float = None):
        '''
        Modify the expected and actual measurements of nth item of measuremnts dictionary
        Arg:
            nth_measurements (dict): nth point in measurements dictionary
            ie) {'expected' : float, 'actual' : float}
            expected (float): expeceted measurements
            actual (float): actual measurements
        Return:
            N/A
        '''
        nth_measurements['input_unit'] = input_unit
        nth_measurements['expected_out'] = expected
        nth_measurements['actual_out'] = actual
