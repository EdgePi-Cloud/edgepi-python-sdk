'''
Provides a class for interacting with the EdgePi Thermocouple via SPI. 
'''

import logging
from edgepi.peripherals.spi import SpiDevice

_logger = logging.getLogger(__name__)

class EdgePiTC(SpiDevice):
    ''' 
    A class used to represent the EdgePi Thermocouple as an SPI device.
    '''
    def __init__(self):
        super().__init__(bus_num=6, dev_ID=0)

    def set_averaging_mode(self, num_samples:int=1):
        '''
        Sets number of measurements made per sampling event.   
        Parameters: and interger from the set {1, 2, 4, 8, 16}. Default = 1. 
        '''
        pass

    def single_sample(self, file_path:str=""):
        '''
        Conduct a single sampling event. Returns measured temperature in degrees Celsius.
        Parameters: a string representing a file path to log results to (optional).
        '''
        pass

    def auto_sample(self, file_path:str=""):
        '''
        Conduct sampling events continuously. Returns measured temperature in degrees Celsius.
        Parameters: a string representing a file path to log results to (optional).
        '''
        pass

    def set_type(self, tc_type:str):
        '''
        Set thermocouple type. 
        Parameters: a string from the set {B,E,J,K,N,R,S,T}.
        '''
        pass
