'''
OpCodes for thermocouple configuration and command operations
'''

from enum import Enum, unique
from edgepi.reg_helper.reg_helper import OpCode

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

class Masks(Enum):
    CR0_BIT0_MASK = 0xFE
    CR0_BIT1_MASK = 0xFD
    CR0_BIT2_MASK = 0xFB
    CR0_BIT3_MASK = 0xF7
    CR0_OC_MASK = 0xCF
    CR0_BIT6_MASK = 0xBF
    CR0_BIT7_MASK = 0x7F
    CR1_HIGH_MASK = 0x0F
    CR1_LOW_MASK = 0xF0

@unique
class TCOps(Enum):
    ''' valid opcodes for commands that can be sent to thermocouple '''
    SINGLE_SHOT = OpCode(0x40, TCAddresses.CR0_W.value, Masks.CR0_BIT6_MASK.value)      # trigger a single temperature conversion
    CLEAR_FAULTS = OpCode(0x02, TCAddresses.CR0_W.value, Masks.CR0_BIT6_MASK.value)     # clear fault status register, only use with Interrupt Fault Mode

@unique
class DecBits(Enum):
    ''' valid decimal values for temperature registers with precision up to 2^-4. '''
    # TODO: add entire range of valid values (16 total)
    p0 = 0
    p1 = 0.5
    p2 = 0.75
    p3 = 0.875
    p4 = 0.9375

@unique
class ConvMode(Enum):
    ''' valid opcodes for setting thermocouple conversion mode '''
    SINGLE = OpCode(0x00, TCAddresses.CR0_W.value, Masks.CR0_BIT7_MASK.value)
    AUTO = OpCode(0x80, TCAddresses.CR0_W.value, Masks.CR0_BIT7_MASK.value)

@unique
class CJMode(Enum):
    ''' valid opcodes for setting thermocouple cold junction mode'''
    ENABLE = OpCode(0x00, TCAddresses.CR0_W.value, Masks.CR0_BIT3_MASK.value)
    DISABLE = OpCode(0x08, TCAddresses.CR0_W.value, Masks.CR0_BIT3_MASK.value)

@unique
class FaultMode(Enum):
    ''' valid opcodes for setting thermocouple fault mode '''
    COMPARATOR = OpCode(0x00, TCAddresses.CR0_W.value, Masks.CR0_BIT2_MASK.value)
    INTERRUPT = OpCode(0x04, TCAddresses.CR0_W.value, Masks.CR0_BIT2_MASK.value)

@unique
class NoiseFilterMode(Enum):
    ''' valid opcodes for setting thermocouple noise rejection filter mode '''
    Hz_60 = OpCode(0x00, TCAddresses.CR0_W.value, Masks.CR0_BIT0_MASK.value)  
    Hz_50 = OpCode(0x01, TCAddresses.CR0_W.value, Masks.CR0_BIT0_MASK.value)

@unique
class AvgMode(Enum):
    ''' valid opcodes for setting thermocouple conversion averaging mode '''
    AVG_1 = OpCode(0x00, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)     # single sample
    AVG_2 = OpCode(0x10, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)     # 2 samples averaged
    AVG_4 = OpCode(0x20, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)     # 4 samples averaged
    AVG_8 = OpCode(0x30, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)     # 8 samples averaged
    AVG_16 = OpCode(0x40, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)    # 16 samples averaged

@unique
class TCType(Enum):
    ''' valid opcodes for setting thermocouple type '''
    TYPE_B = OpCode(0x00, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)     # type B thermocouple
    TYPE_E = OpCode(0x01, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)     # type E thermocouple
    TYPE_J = OpCode(0x02, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)     # type J thermocouple
    TYPE_K = OpCode(0x03, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)     # type K thermocouple
    TYPE_N = OpCode(0x04, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)     # type N thermocouple
    TYPE_R = OpCode(0x05, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)     # type R thermocouple
    TYPE_S = OpCode(0x06, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)     # type S thermocouple
    TYPE_T = OpCode(0x07, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)     # type T thermocouple

class VoltageMode(Enum):
    ''' valid opcodes for setting thermocouple voltage mode '''
    GAIN_8 = OpCode(0x08, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)
    GAIN_32 = OpCode(0x0C, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)

class FaultMasks(Enum):
    ''' valid opcodes for setting thermocouple fault masks '''
