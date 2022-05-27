'''
Provides a class for interacting with the EdgePi Thermocouple via SPI. 
'''

import logging
from edgepi.peripherals.spi import SpiDevice
from edgepi.tc import tc_constants as tc

_logger = logging.getLogger(__name__)


class EdgePiTC(SpiDevice):
    ''' 
    A class used to represent the EdgePi Thermocouple as an SPI device.
    '''

    def __init__(self):
        super().__init__(bus_num=6, dev_ID=0)

    # TODO: use enum instead of int
    def set_averaging_mode(self, num_samples:tc.AVG_MODE):
        '''
        Sets number of measurements made per sampling event.   
        Parameters: and interger from the set {1, 2, 4, 8, 16}. Default = 1. 
        '''
        pass

    def single_sample(self, file_path:str=None):
        '''
        Conduct a single sampling event. Returns measured temperature in degrees Celsius.
        Parameters: a string representing a file path to log results to (optional).
        '''
        pass

    def auto_sample(self, file_path:str=None):
        '''
        Conduct sampling events continuously. Returns measured temperature in degrees Celsius.
        Parameters: a string representing a file path to log results to (optional).
        '''
        pass

    def set_type(self, tc_type:tc.TC_TYPE):
        '''
        Set thermocouple type. 
        Parameters: a string from the set {B,E,J,K,N,R,S,T}.
        '''
        pass

    def set_config(
        self,
        conversion_mode: tc.CONV_MODE = None,  
        oc_fault_mode: tc.FAULT_MODE = None, 
        cold_junction_mode: tc.CJ_MODE = None, 
        fault_mode: tc.FAULT_MODE = None,
        noise_filter_mode: tc.NOISE_FILTER_MODE = None,
        average_mode: tc.AVG_MODE = None,
        tc_type: tc.TC_TYPE = None,
        voltage_mode: tc.VOLT_MODE = None,
        fault_mask: tc.FAULT_MASKS = None,
        cj_high_threshold: int=None,
        cj_low_threshold: int=None,
        lt_high_threshold: int=None,
        lt_high_threshold_decimals: tc.DEC_BITS = None,
        lt_low_threshold: int=None,
        lt_low_threshold_decimals: tc.DEC_BITS=None,
        cj_offset: int=None,
        cj_offset_decimals: tc.DEC_BITS=None,
        ):
        pass
