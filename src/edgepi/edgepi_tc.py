from edgepi.peripherals.spi import SpiDevice

import logging
_logger = logging.getLogger(__name__)

class EdgePiTC(SpiDevice):
    def __init__(self):
        super().__init__(bus_num=6, dev_ID=0)

    ''' Set number of replications per sampling event. Options: 1, 2, 4, 8, 16. Default = 1. '''
    def set_averaging_mode(self, num_samples:int=1):
        pass

    ''' Conduct a single sampling event. Returns measured temperature in degrees Celsius. Optional log results to file. '''
    def single_sample(self, file_path:str=""):
        pass

    ''' Conduct sampling events continuously for the specified period of time. Optional log results to file.'''
    def auto_sample(self, file_path:str=""):
        pass

    ''' Select thermocouple type. Options: B,E,J,K,N,R,S,T. '''
    def set_type(self, tc_type:str):
        pass
