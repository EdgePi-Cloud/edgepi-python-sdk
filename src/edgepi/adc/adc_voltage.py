"""ADC voltage reading configuration and utility methods"""


import logging

from bitstring import BitArray


# TODO: retrieve these values from EEPROM once added
STEP_DOWN_RESISTOR_1 = 19.1
STEP_DOWN_RESISTOR_2 = 4.99


_logger = logging.getLogger()


def _is_negative_voltage(code: BitArray):
    """
    Determines if voltage code is negative value
    """
    return code[0] == 1


def _code_to_input_voltage(code: int, v_ref: float, num_bits: int):
    """
    Converts digital code obtained from ADC voltage read to
    ADC input voltage (i.e. voltage measured at ADC) based on voltage range
    provided by reference voltage
    """
    voltage_range = v_ref / 2 ** (num_bits - 1)
    return float(code) * voltage_range


def _input_voltage_to_output_voltage(v_in: float, gain: float, offset: float):
    """
    Converts ADC input voltage (i.e. voltage measured at ADC) to
    ADC output voltage (i.e. voltage measured at terminal block)
    """
    step_up_ratio = (STEP_DOWN_RESISTOR_1 + STEP_DOWN_RESISTOR_2) / STEP_DOWN_RESISTOR_2
    return v_in * step_up_ratio * gain - offset


def code_to_voltage(code: BitArray, adc_info):
    """
    Converts ADC voltage read digital code to output voltage (voltage measured at terminal block)

    Args:
        code (BitArray): bitstring representation of digital code retrieved from ADC voltage read

        adc_info (ADCReadInfo): data about this adc's voltage reading configuration
    """
    num_bits = adc_info.num_data_bytes * 8
    config = adc_info.voltage_config

    # code is given in 2's complement, remove leading 1
    if _is_negative_voltage(code):
        code[0] = 0

    v_in = _code_to_input_voltage(code.uint, config.v_ref, num_bits)

    v_out = _input_voltage_to_output_voltage(v_in, config.gain, config.offset)

    return v_out

class CRCError(Exception):
    """Raised if CRC check fails to match CRC code generated by ADS1263"""

def crc_8_atm(value: int, frame_len: int, code: int):
    """
    Performs Cyclic Redundancy Check using the CRC-8-ATM polynomial.

    See ADS1263 documentation, p.72 for details on CRC-8-ATM algorithm.

    Args:
        value (int): uint value of the voltage read data (either 3 or 4 bytes)

        frame_len (int): num bits in voltage read data (either 3 or 4 bytes)

        code (int): 8-bit CRC-8-ATM code generated by ADS1263 for voltage data

    Returns:
        int: uint 8-bit CRC value
    """
    crc = 0b100000111   # CRC-8-ATM polynomial
    crc_len = 9         # num bits in CRC-8-ATM polynomial
    _logger.info(f"\nExpected CRC Code:\t\t{hex(crc)}")

    # pad value with zeros (to ensure 8-bit code returned)
    _logger.debug(f"Initial Value:\t\t{bin(value)}")
    value <<= (crc_len - 1)
    _logger.debug(f"Paddded Value:\t\t{bin(value)}")

    # align crc polynomial to leading 1 of value
    _logger.debug(f"Initial CRC:\t\t{bin(crc)}")
    crc <<= (frame_len - 1)
    _logger.debug(f"Padded CRC:\t\t{bin(crc)}")

    # flag is used to find leading 1 in value.
    # frame_len is either 32 or 24, so bit flag must be
    # 40 or 32 bits (value was padded with 8 bits in first step)
    flag = 0b1 << (frame_len + 7)
    _logger.debug(f"Padded Flag:\t\t{bin(flag)}")

    # stop crc once XOR'd value is less than 0x100 (get 8-bit code)
    while value >= 0x100:
        _logger.debug("\n----- New CRC Iteration -----")
        _logger.debug(f"Flag:\t\t{bin(flag)}")
        _logger.debug(f"CRC:\t\t{bin(crc)}")
        _logger.debug(f"Value:\t\t{bin(value)}")

        # locate leading 1 in value and align CRC polynomial to leading 1
        while not value & flag:
            flag >>= 1
            crc >>= 1
        _logger.debug(f"Shifted Flag:\t\t{bin(flag)}")
        _logger.debug(f"Shifted CRC:\t\t{bin(crc)}")

        # now CRC's msb is aligned to leading 1 of value, XOR them
        value ^= (crc)

        _logger.debug(f"XOR'd Value:\t\t{bin(value)}")
        _logger.debug("-------------------------")

    if value != code:
        raise CRCError(f"CRC check failed: computed code {hex(value)} != expected {hex(code)}")

    _logger.info(f"\nComputed CRC Code:\t\t{hex(value)}")
    return value
