from dataclasses import dataclass
from enum import Enum, unique

@unique
class TCAddresses(Enum):
    # Read addresses
    CR0_R = 0x00
    CR1_R = 0x01
    MASK_R = 0x02
    CJHF_R = 0x03
    CJLF_R = 0x04
    LTHFTH_R = 0x05
    LTHFTL_R = 0x06
    LTLFTH_R = 0x07
    LTLFTL_R = 0x08
    CJTO_R = 0x09
    CJTH_R = 0x0A
    CJTL_R = 0x0B
    LTCBH_R = 0x0C
    LTCBM_R = 0x0D
    LTCBL_R = 0x0E
    SR_R = 0x0F

    # Write addresses
    CR0_W = 0x80
    CR1_W = 0x81
    MASK_W = 0x82
    CJHF_W = 0x83
    CJLF_W = 0x84
    LTHFTH_W = 0x85
    LTHFTL_W = 0x86
    LTLFTH_W = 0x87
    LTLFTL_W = 0x88
    CJTO_W = 0x89
    CJTH_W = 0x8A
    CJTL_W = 0x8B

@unique
class TCOps(Enum):
    ''' valid hex opcodes for commands that can be sent to thermocouple '''
    SINGLE_SHOT = 0x40      # trigger a single temperature conversion
    CLEAR_FAULTS = 0x02     # clear fault status register, only use with Interrupt Fault Mode

@dataclass
class DecBits:
    ''' valid decimal values for temperature registers with precision up to 2^-4. '''
    # TODO: add entire range of valid values (16 total)
    p0 = 0
    p1 = 0.5
    p2 = 0.75
    p3 = 0.875
    p4 = 0.9375

@unique
class ConvMode(Enum):
    ''' valid hex opcodes for setting thermocouple conversion mode '''
    SINGLE = 0x7F
    AUTO = 0x80

@unique
class CJMode(Enum):
    ''' valid hex opcodes for setting thermocouple cold junction mode'''
    ENABLE = 0xF7
    DISABLE = 0x08

@unique
class FaultMode(Enum):
    ''' valid hex opcodes for setting thermocouple fault mode '''
    COMPARATOR = 0xFB
    INTERRUPT = 0x04

@unique
class NoiseFilterMode(Enum):
    ''' valid hex opcodes for setting thermocouple noise rejection filter mode '''
    Hz_60 = 0xFE
    Hz_50 = 0x01

@unique
class AvgMode(Enum):
    ''' valid hex opcodes for setting thermocouple conversion averaging mode '''
    AVG_1 = 0x00         # single sample
    AVG_2 = 0x10         # 2 samples averaged
    AVG_4 = 0x20         # 4 samples averaged
    AVG_8 = 0x30         # 8 samples averaged
    AVG_16 = 0x40        # 16 samples averaged

@unique
class TCType(Enum):
    ''' valid hex opcodes for setting thermocouple type '''
    TYPE_B = 0x00            # type B thermocouple
    TYPE_E = 0x01            # type E thermocouple
    TYPE_J = 0x02            # type J thermocouple
    TYPE_K = 0x03            # type K thermocouple
    TYPE_N = 0x04            # type N thermocouple
    TYPE_R = 0x05            # type R thermocouple
    TYPE_S = 0x06            # type S thermocouple
    TYPE_T = 0x07            # type T thermocouple

class VoltageMode(Enum):
    ''' valid hex opcodes for setting thermocouple voltage mode '''
    GAIN_8 = 0x08
    GAIN_32 = 0x0C

class FaultMasks(Enum):
    ''' valid hex opcodes for setting thermocouple fault masks '''
