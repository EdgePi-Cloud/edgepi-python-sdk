'''
Module for importing calibration paratmeter
from the external eeprom
'''

from edgepi.calibration.eeprom_constants import (
    ModuleNames,
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
            ie) {1: {0 : {'input_unit' : int, 'expected_out' : float, 'actual_out' : float},
                 .   .
                 .   .
                 .   .
                 .  nth_point : {'input_unit' : int, 'expected_out' : float, 'actual_out' : float}}
                 .
               nth_ch : {0 : {'input_unit' : int, 'expected_out' : float, 'actual_out' : float},
                           .
                           .
                           .
                        nth_point : {'input_unit' : int, 'expected_out' :float,'actual_out':float}}}
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

    def least_square_regression(self, ch_meas_dict: dict = None, ch_calib_dict: dict = None):
        '''
        Comput Calibration parameters using least square regression method
        Args:
            ch_meas_dict (dict): channel measurements dictionary which stores measured data at each
            input code value
            ch_calib_dict (dict): channel calibration dictionary which stores calibration parameter
            for each channel
        Return:
            N/A
        '''
        dt_ptn_len = len(ch_meas_dict[0].keys())

        _x, _xx, _y, _xy = self.prepare_variable_list(ch_meas_dict)

        for ch in range(self.num_of_ch):
            gain = ((dt_ptn_len*sum(_xy[ch])) - (sum(_x)*sum(_y[ch]))) / \
                    (dt_ptn_len*sum(_xx) - sum(_x)**2)
            offset = (sum(_y[ch])-gain*sum(_x))/dt_ptn_len
            ch_calib_dict[ch].gain = gain
            ch_calib_dict[ch].offset = offset

    def prepare_variable_list(self, ch_meas_dict: dict = None):
        '''
        Compute list of variables used in least square regression formula. x, y, xy, xx
        Args:
            ch_meas_dict (dict): channel measurements dictionary which stores measured data at each
            input code value
         Return:
            x (list): list of inputs, code value for DAC module, voltage for ADC module
            y (list): list of outpus, voltage value for DAC module, code value for ADC module
            xy (list): list of x[n] * y[n], element wise multiplication
            xx (list): x squared
        '''
        _x = list(ch_meas_dict[0].keys())
        _xx = [key**2 for key in ch_meas_dict[0].keys()]

        _y =   []
        _xy =  []

        for ch in range(self.num_of_ch):
            _y.append([actual_out['actual_out'] for _, actual_out in ch_meas_dict[ch].items()])
            _xy.append([x_n * y_n for x_n, y_n in zip(_x, _y[ch])])

        return _x, _xx, _y, _xy
