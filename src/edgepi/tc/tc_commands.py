import logging
from edgepi.tc.tc_constants import *

_logger = logging.getLogger(__name__)

class TCCommands():  
    def temp_to_code(self, temp:float):
        ''' converts a float temperature value to binary code for writing to register '''
        pass

    def code_to_temp(self, code_bytes:list):
        ''' converts register binary temperature code to float value'''
        # generate cold junction temperature and linearized TC temperatures
        try:
            cj_high_byte = code_bytes[1]
            cj_low_byte = code_bytes[2]
            lt_high_byte = code_bytes[3]
            lt_mid_byte = code_bytes[4]
            lt_low_byte = code_bytes[5]
        except IndexError:
            _logger.error(f'single sample failed to read registers')
            return None

        # combine code bytes and eliminate unneeded bits
        cj_code = ((cj_high_byte<<8) + cj_low_byte) >> 2
        # check if code is negative value and update value
        if cj_high_byte & 0x80:
            cj_code -= 2 << (14 - 1)

        # combine code bytes and eliminate unneeded bits
        lt_code = ((lt_high_byte<<16) + (lt_mid_byte<<8) + lt_low_byte) >> 5
        # check if code is negative value and update value
        if lt_high_byte & 0x80:
            lt_code -= 2 << (19 - 1)

        _logger.info(f'Cold Junction Temp: {cj_code*(2**-6)}')  # >> shift the 6 precision bits behind the decimal point
        _logger.info(f'LT TC Temp: {lt_code*(2**-7)}')          # >> shift the 7 precision bits behind the decimal point

        return cj_code, lt_code
    