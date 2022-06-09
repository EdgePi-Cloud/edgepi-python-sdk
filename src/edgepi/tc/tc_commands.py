import logging
from edgepi.tc.tc_constants import *

_logger = logging.getLogger(__name__)

class TCCommands():  
    def temp_to_code(self, temp:float):
        ''' converts a float temperature value to binary code for writing to register '''
        pass
    
    def __negative_temp_check(self, temp_code, temp_code_high_byte, temp_bits):
        # if sign bit is set (negative temp), toggle sign bit off. Compute as positive and then invert after.
        if temp_code_high_byte & 0x80:
            temp_code ^= (0x1 << (temp_bits-1))
        return temp_code

    def code_to_temp(self, code_bytes:list):
        ''' converts cold junction and linearized thermocouple temperature binary codes to float values'''
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

        # combine and arrange the temperature bits in order from msb to lsb and eliminate empty placeholder bits
        cj_code = ((cj_high_byte<<8) + cj_low_byte) >> 2
        cj_code = self.__negative_temp_check(cj_code, cj_high_byte, TempBits.CJ_BITS.value)

        # combine and arrange the temperature bits in order from msb to lsb and eliminate empty placeholder bits
        lt_code = ((lt_high_byte<<16) + (lt_mid_byte<<8) + lt_low_byte) >> 5
        lt_code = self.__negative_temp_check(lt_code, lt_high_byte, TempBits.LT_BITS.value)

        cj_temp = cj_code*(2**-TempBits.CJ_DECIMAL_BITS.value)   # >> shift the 6 precision bits behind the decimal point
        lt_temp = lt_code*(2**-TempBits.LT_DECIMAL_BITS.value)   # >> shift the 7 precision bits behind the decimal point

        # invert if negative temperature
        if cj_high_byte & 0x80:
            cj_temp = 0 - cj_temp
        if lt_high_byte & 0x80:
            lt_temp = 0 - lt_temp

        _logger.info(f'Cold Junction Temp: {cj_temp}')  
        _logger.info(f'LT TC Temp: {lt_temp}')         

        return cj_temp, lt_temp
    