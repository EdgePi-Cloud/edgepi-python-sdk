'''
Module for importing calibration paratmeter
from the external eeprom
'''

import numbers
from edgepi.calibration.eeprom_constants import (
    ModuleNames,
)
from edgepi.calibration.calibration_constants import(
    NumOfCh,
    CalibParam,
    ReferenceV
)

# TODO: calibration class should only handle the calibration process and separate the data storage

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

    def __generate_calib_param_dict(self):
        '''
        Function to generate dictionary of calibration parameters
        Args:
            N/A
        Return:
            ch_to_calib_dict (dict): dictionary mapped channel to CalibParam data class
            ie) {1 : CalibParam(gain, offset)}
        '''
        ch_to_calib_dict = {}
        for ch in range(self.num_of_ch):
            ch_to_calib_dict[ch] = CalibParam(gain=1, offset=0)
        return ch_to_calib_dict

    def __generate_measurements_dict(self, num_of_points):
        '''
        Function to generate dictionary of measurements to generate calibration parameter. It will
        store expected and actual measurements at each data point for number_of_points length
        Args:
            num_of_points (int): number of points to be generated, used as length of the dictionary
        Return:
            measurements_dict (dict): dictionary mapping expected value to 
        '''
        measurements_dict = {}
        for point in range(num_of_points):
            measurements_dict[point]= {'expected': 0, 'actual': 0}
        return measurements_dict

#TODO:  Least Square method
