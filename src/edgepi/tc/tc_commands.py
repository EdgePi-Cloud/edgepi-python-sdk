import logging
import bitstring
from edgepi.tc.tc_constants import *

_logger = logging.getLogger(__name__)
  
def temp_to_code(temp:float):
    ''' converts a float temperature value to binary code for writing to register '''
    raise NotImplementedError

def _negative_temp_check(temp_code):
    # if sign bit is set (negative temp), toggle sign bit off. Compute as positive and then invert after.
    if temp_code[0]:
        del temp_code[0]
        return True
    return False

def code_to_temp(code_bytes:list):
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

    cj_negative_flag, lt_negative_flag = False, False

    # combine and arrange the temperature bits in order from msb to lsb and eliminate empty placeholder bits
    cj_code = bitstring.pack('uint:8, uint:8', cj_high_byte, cj_low_byte)
    del(cj_code[-2:])
    cj_negative_flag = _negative_temp_check(cj_code)

    # combine and arrange the temperature bits in order from msb to lsb and eliminate empty placeholder bits
    lt_code = bitstring.pack('uint:8, uint:8, uint:8', lt_high_byte, lt_mid_byte, lt_low_byte)
    del(lt_code[-5:])
    lt_negative_flag = _negative_temp_check(lt_code)

    cj_temp = cj_code.uint * (2**-TempBits.CJ_DECIMAL_BITS.value)   # >> shift the 6 precision bits behind the decimal point
    lt_temp = lt_code.uint * (2**-TempBits.LT_DECIMAL_BITS.value)   # >> shift the 7 precision bits behind the decimal point

    # invert if negative temperature
    if cj_negative_flag:
        cj_temp = -(cj_temp)
    if lt_negative_flag:
        lt_temp = -(lt_temp)

    _logger.info(f'Cold Junction Temp: {cj_temp}')  
    _logger.info(f'LT TC Temp: {lt_temp}')         

    return cj_temp, lt_temp
    