'''
Utility module for computing MAX31856 conversion time

Functions:
    calc_conv_time(int, int, bool)
'''


from enum import Enum
from bitstring import Bits

SAFETY_MARGIN = 1.1


class ConvTimes(Enum):
    """Converson time delays for various MAX31856 settings configurations"""

    CJ_ON_OC_LOW_NOM = 13.3
    CJ_ON_OC_LOW_MAX = 15
    CJ_ON_OC_MED_NOM = 33.4
    CJ_ON_OC_MED_MAX = 37
    CJ_ON_OC_HIGH_NOM = 113.4
    CJ_ON_OC_HIGH_MAX = 125
    CJ_OFF_OC_LOW_NOM = 40
    CJ_OFF_OC_LOW_MAX = 44
    CJ_OFF_OC_MED_NOM = 60
    CJ_OFF_OC_MED_MAX = 66
    CJ_OFF_OC_HIGH_NOM = 140
    CJ_OFF_OC_HIGH_MAX = 154
    CJ_OFF = -25.0
    DEFAULT_HZ50_NOM = 169
    DEFAULT_HZ50_MAX = 185
    DEFAULT_HZ60_NOM = 143
    DEFAULT_HZ60_MAX = 155
    HZ50_AVG_2 = 40.33
    HZ50_AVG_4 = 120.99
    HZ50_AVG_8 = 282.31
    HZ50_AVG_16 = 604.95
    HZ60_AVG_2 = 33.33
    HZ60_AVG_4 = 99.99
    HZ60_AVG_8 = 233.31
    HZ60_AVG_16 = 499.95


_open_circ_delays = {
    0b100: (0, 0),
    0b101: (ConvTimes.CJ_OFF_OC_LOW_NOM.value, ConvTimes.CJ_OFF_OC_LOW_MAX.value),
    0b110: (ConvTimes.CJ_OFF_OC_MED_NOM.value, ConvTimes.CJ_OFF_OC_MED_MAX.value),
    0b111: (ConvTimes.CJ_OFF_OC_HIGH_NOM.value, ConvTimes.CJ_OFF_OC_HIGH_MAX.value),
    0b000: (0, 0),
    0b001: (ConvTimes.CJ_ON_OC_LOW_NOM.value, ConvTimes.CJ_ON_OC_LOW_MAX.value),
    0b010: (ConvTimes.CJ_ON_OC_MED_NOM.value, ConvTimes.CJ_ON_OC_MED_MAX.value),
    0b011: (ConvTimes.CJ_ON_OC_HIGH_NOM.value, ConvTimes.CJ_ON_OC_HIGH_MAX.value),
}

_default_times = {
    0b0: (ConvTimes.DEFAULT_HZ60_NOM.value, ConvTimes.DEFAULT_HZ60_MAX.value),
    0b1: (ConvTimes.DEFAULT_HZ50_NOM.value, ConvTimes.DEFAULT_HZ50_MAX.value),
}

_avg_mode_delays = {
    0b00000: 0,
    0b10000: 0,
    0b00001: ConvTimes.HZ60_AVG_2.value,
    0b00010: ConvTimes.HZ60_AVG_4.value,
    0b00011: ConvTimes.HZ60_AVG_8.value,
    0b00100: ConvTimes.HZ60_AVG_16.value,
    0b10001: ConvTimes.HZ50_AVG_2.value,
    0b10010: ConvTimes.HZ50_AVG_4.value,
    0b10011: ConvTimes.HZ50_AVG_8.value,
    0b10100: ConvTimes.HZ50_AVG_16.value,
}


def calc_conv_time(cr0_val: int, cr1_val: int, safe_delay: bool = True):
    """Computes the time delay required for thermocouple single sampling

    Args:
        cr0_val (int): the value stored in register CR0

        cr1_val (int): the value stored in register CR1

        safe_delay (bool): indicator for whether to compute min or max time delay

    Returns:
        a float representing the computed time delay in milliseconds (ms)
    """
    cr0 = Bits(uint=cr0_val, length=8)
    cr1 = Bits(uint=cr1_val, length=8)
    noise_filt_bit = cr0[7]
    cold_junct_bit = cr0[4]
    open_circ_bits = cr0[2:4]
    avg_mode_bits = cr1[0:4]

    conv_time = 0

    # format bit strings for various modes
    open_circ_bit_str = [cold_junct_bit] + open_circ_bits
    avg_mode_bit_str = [noise_filt_bit] + avg_mode_bits

    # compute conv time for settings that depend on safety margin
    if safe_delay:
        conv_time += _default_times[noise_filt_bit][1]  # base conv time
        conv_time += _open_circ_delays[open_circ_bit_str.uint][1]  # open circuit test delay
    else:
        conv_time += _default_times[noise_filt_bit][0]  # base conv time
        conv_time += _open_circ_delays[open_circ_bit_str.uint][0]  # open circuit test delay

    if cold_junct_bit:
        conv_time += ConvTimes.CJ_OFF.value

    # additional conv time delays
    conv_time += _avg_mode_delays[avg_mode_bit_str.uint]

    return conv_time * SAFETY_MARGIN
