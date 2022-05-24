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
        ''' Set number of replications per sampling event. Options: 1, 2, 4, 8, 16. Default = 1. '''
        pass

    def single_sample(self, file_path:str=""):
        ''' Conduct a single sampling event. Returns measured temperature in degrees Celsius. Optional log results to file. '''
        pass

    def auto_sample(self, file_path:str=""):
        ''' Conduct sampling events continuously for the specified period of time. Optional log results to file. '''
        pass

    def set_type(self, tc_type:str):
        ''' Select thermocouple type. Options: B,E,J,K,N,R,S,T. '''
        pass
