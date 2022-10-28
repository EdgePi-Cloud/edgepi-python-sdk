'''
Module for generating calibration parameter data structure for each module. This module should be
able to generate new calibration parameters using measurements tools.
'''

from struct import pack

from edgepi.calibration.eeprom_constants import (
    ModuleNames,
    MemoryAddr
)
from edgepi.calibration.calibration_constants import(
    NumOfCh,
    CalibParam,
    # ReferenceV
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
        self.full_scale_range = None
        self.full_scale_code = None

# TODO: to be used for prepare a value to be upkoaded to eeprom
# pylint: disable=unused-private-member
    def __from_value_to_memory(self, param: float = None):
        param = int(param*10**9)
        value = pack("i", param)
        return list(value)

    def __from_memory_to_value(self, memory: list = None) -> float:
        value = pack("BBBB", memory[0], memory[1], memory[2], memory[3])
        value = int.from_bytes(value, "little", signed=True)
        return float(format(value*10**-9, '.9f'))

    def __generat_dac_calib_dict(self, calib_param: list = None) :
        '''
        Function to generate DAC calibration parameter dictionary based on the list of imported cal-
        ibration parameter from DAC module.

        Arg:
            calib_param (list): list contains the parameter read from eeprom and passed from each mo
            -dule
        Return:
            calib_dict (dict):
        '''
        calib_dict={}
        for ch in range(self.num_of_ch):
            offset = ch * MemoryAddr.CH_OFFSET.value
            packed_gain = self.__from_memory_to_value(calib_param[offset:offset+4])
            packed_offset = self.__from_memory_to_value(calib_param[offset+4:offset+8])
            calib_dict[ch] = CalibParam(gain = packed_gain, offset=packed_offset)

        return calib_dict

# TODO: ADC Calib to be added
    # def __generat_adc_calib_dict(self, calib_param: list = None) :
    #     '''
    #     Function to generate ADC calibration parameter dictionary based on the list of imported
    #     calibration parameter from ADC module.

    #     Arg:
    #         calib_param (list): list contains the parameter read from eeprom and passed from each
    #         module
    #     Return:
    #         calib_dict (dict):
    #     '''

    #     return 2

# TODO: RTD Calib to be added
    # def __generat_rtd_calib_dict(self, calib_param: list = None) :
    #     '''
    #     Function to generate RTD calibration parameter dictionary based on the list of imported
    #     calibration parameter from RTD module.

    #     Arg:
    #         calib_param (list): list contains the parameter read from eeprom and passed from each
    #         module
    #     Return:
    #         calib_dict (dict):
    #     '''

    #     return 3

# TODO: TC Calib to be added
    # def __generat_tc_calib_dict(self, calib_param: list = None) :
    #     '''
    #     Function to generate TC calibration parameter dictionary based on the list of imported
    #     calibration parameter from TC module.

    #     Arg:
    #         calib_param (list): list contains the parameter read from eeprom and passed from each
    #         module
    #     Return:
    #         calib_dict (dict):
    #     '''

    #     return 4

    def get_calibration_dict(self, calib_param: list = None):
        '''
        Function to generate calibration parameter dictionary based on the list of imported
        calibration parameter from each module.

        Arg:
            calib_param (list): list contains the parameter read from eeprom and passed from each
            module
        Return:
            calib_dict (dict):
        '''
        calib_dict = 0
        if self.module == ModuleNames.DAC.value:
            calib_dict = self.__generat_dac_calib_dict(calib_param)
        # elif self.module == ModuleNames.ADC.value:
        #     calib_dict = self.__generat_adc_calib_dict(calib_param)
        # elif self.module == ModuleNames.RTD.value:
        #     calib_dict = self.__generat_rtd_calib_dict(calib_param)
        # elif self.module == ModuleNames.TC.value:
        #     calib_dict = self.__generat_tc_calib_dict(calib_param)
        return calib_dict

    def generate_calib_param_dict(self):
        '''
        Function to generate dictionary of calibration parameters
        Args:
            N/A
        Return:
            ch_to_calib_dict (dict): dictionary mapped channel to CalibParam data class
            ie) {1 : CalibParam(gain, offset)
                 .
                 .
                 .
                 nth_channel : CalibParam(gain, offset)}
        '''
        ch_to_calib_dict = {}
        for ch in range(self.num_of_ch):
            ch_to_calib_dict[ch] = CalibParam(gain=1, offset=0)
        return ch_to_calib_dict

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
