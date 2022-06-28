from enum import Enum, unique
import logging
from dataclasses import dataclass
from bitstring import BitArray, pack
from edgepi.tc.tc_constants import DecBits4, TempBits, Masks
from edgepi.reg_helper.reg_helper import OpCode

_logger = logging.getLogger(__name__)
  
def temp_to_code(temp:float):
    ''' converts a float temperature value to binary code for writing to register '''
    raise NotImplementedError

def _negative_temp_check(temp_code:int):
    ''' checks if MAX31856 temperature register reading is negative '''
    # if sign bit is set (negative temp), toggle sign bit off. Compute as positive and then invert after.
    if temp_code[0]:
        del temp_code[0]
        return True
    return False

def code_to_temp(code_bytes:list):
    ''' converts cold junction and linearized thermocouple temperature binary codes to float values'''
    # generate cold junction temperature and linearized TC temperatures
    cj_high_byte = code_bytes[1]
    cj_low_byte = code_bytes[2]
    lt_high_byte = code_bytes[3]
    lt_mid_byte = code_bytes[4]
    lt_low_byte = code_bytes[5]

    cj_negative_flag, lt_negative_flag = False, False

    # combine and arrange the temperature bits in order from msb to lsb and eliminate empty placeholder bits
    cj_code = pack('uint:8, uint:8', cj_high_byte, cj_low_byte)
    del(cj_code[-2:])
    cj_negative_flag = _negative_temp_check(cj_code)

    # combine and arrange the temperature bits in order from msb to lsb and eliminate empty placeholder bits
    lt_code = pack('uint:8, uint:8, uint:8', lt_high_byte, lt_mid_byte, lt_low_byte)
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

@unique
class TempType(Enum):
    CJ = 0
    LT = 1
    CJ_OFF = 2

@dataclass 
class TempCode():
    ''' Holds data needed to update a MAX31856 temperature threshold configuration, where
        configuring this setting requires updating one or more registers whose bits are 
        assigned roles as either sign, integer, decimal, or filler bits.

        Attributes:
            int_val (int): the integer value to be written to this setting 

            dec_val (DecBits): the decimal value to be written to this setting, represented
                            as a binary value (uint)
            
            num_int_bits (int): the number of bits assigned to integer values for this setting

            num_dec_bits (int): the number of bits assigned to decimal values for this setting

            num_int_bits (int): the number of bits assigned to filler values for this setting

            start_addx (int): address of the MSB for this setting

            setting_name (TempType): the name for this temperature setting
    '''
    int_val : int
    dec_val : int
    num_int_bits : int
    num_dec_bits : int
    num_filler_bits: int
    start_addx: int
    setting_name: TempType

    def check_values(self):
        if self.int_val is None:
            self.int_val = 0
        elif self.dec_val is None:
            self.dec_val = DecBits4.P0

def _format_temp_bitstring(sign_bit:int, int_val:int, dec_val:int, num_int_bits:int, num_dec_bits:int, fill_bits:int):
    ''' Combine and place in order the sign, int, dec, and filler bits of a TempCode into a BitArray

        Returns:
            a bitstring BitArray ordered from MSB to LSB as a MAX31856 temperature register: sign_bit, int_val, dec_val, fill_bits
    '''
    bits = BitArray(uint=sign_bit, length=1)
    int_bits = BitArray(uint=int_val, length=num_int_bits)
    bits.append(int_bits)
    dec_bits = BitArray(uint=dec_val, length=num_dec_bits) if num_dec_bits else ""
    bits.append(dec_bits)
    for i in range(fill_bits):
        bits += '0b0'
    return bits

def _slice_bitstring_to_opcodes(temp_code:TempCode, bitstr:BitArray, num_slices:int) -> list:
    ''' Uses a bitstring representing a temperature setting update to produce OpCodes
        for carrying out this operation

        Returns:
            a list of OpCodes
    '''
    op_codes = []
    for i in range(num_slices):
        start = i * 8
        end = start + 8
        value = bitstr[start:end].uint
        # create new OpCode, incrementing address to next register each time if
        # this temp_code requires > 1 register.
        op_codes.append(OpCode(value, temp_code.start_addx+i, Masks.BYTE_MASK.value))
    return op_codes
    
def _validate_temperatures(tempcode:TempCode):
    ''' Validates integer value of TempCode is within writeable range for 
        affected register.
    '''
    reg_temps = {
        TempType.CJ.value: {'min': -127, 'max': 127},
        TempType.LT.value: {'min': -2047, 'max': 2047},
        TempType.CJ_OFF.value: {'min': -7, 'max': 7},
    }
    temp_type = tempcode.setting_name.value
    temp_val = tempcode.int_val
    if temp_type in reg_temps:
        if temp_val < reg_temps[temp_type]['min'] or temp_val > reg_temps[temp_type]['max']:
            raise ValueError(f'Temperature integer value {temp_val} exceeds writeable limits for setting {tempcode.setting_name}')


def tempcode_to_opcode(temp_code:TempCode):
    if temp_code is None:
        raise ValueError('temp_code must be of type TempCode: received None')
    
    # no args passed for this temp setting
    if temp_code.int_val is None and temp_code.dec_val is None:
        return []

    # only either int or dec args passed for this temp setting
    if temp_code.int_val is None or temp_code.dec_val is None:
        raise ValueError('temp_code requires both int and dec values: received only one of these.')

    # validate temp range
    _validate_temperatures(temp_code)

    # compute total bits required by this setting
    num_bits = 1 + temp_code.num_int_bits + temp_code.num_dec_bits + temp_code.num_filler_bits

    if num_bits % 8:
        raise ValueError('Number of temp_code bits not divisible by 8 bit register size')

    # check if negative temperature
    sign_bit = 0
    if temp_code.int_val < 0:
        sign_bit = 1 
        temp_code.int_val = abs(temp_code.int_val)

    # combine and place in order the sign, int, dec, and filler bits into a BitArray
    bits = _format_temp_bitstring(sign_bit, temp_code.int_val, temp_code.dec_val.value, temp_code.num_int_bits,
                                temp_code.num_dec_bits, temp_code.num_filler_bits)

    # slice bitstring into 8-bit register sized chunks and convert each chunk to OpCode
    num_regs = int(num_bits / 8) # number of registers this setting uses
    return _slice_bitstring_to_opcodes(temp_code, bits, num_regs)
