"""
OpCodes and Enums for thermocouple configuration and command operations
"""

from enum import Enum, unique
from edgepi.reg_helper.reg_helper import OpCode

REG_SIZE = 8  # MAX31856 register size in bits
NUM_WRITE_REGS = 12 # Number of MAX31856 writeable registers


@unique
class TCAddresses(Enum):
    """Valid hexadecimal address values for MAX31856 registers"""

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
    """values for clearing or 'masking' register bits"""

    BIT0_MASK = 0xFE
    BIT1_MASK = 0xFD
    BIT2_MASK = 0xFB
    BIT3_MASK = 0xF7
    BIT4_MASK = 0xEF
    BIT5_MASK = 0xDF
    BIT6_MASK = 0xBF
    BIT7_MASK = 0x7F
    CR0_OC_MASK = 0xCF
    CR1_HIGH_MASK = 0x0F
    CR1_LOW_MASK = 0xF0
    BYTE_MASK = 0x00


@unique
class TempBits(Enum):
    """number of bits used in MAX31856 temperature registers to store values"""

    CJ_BITS = 14
    LT_BITS = 19
    CJ_DECIMAL_BITS = 6
    LT_DECIMAL_BITS = 7


@unique
class TCOps(Enum):
    """valid opcodes for commands that can be sent to thermocouple"""

    SINGLE_SHOT = OpCode(
        0x40, TCAddresses.CR0_W.value, Masks.BIT6_MASK.value
    )  # trigger a single temperature conversion
    CLEAR_FAULTS = OpCode(
        0x02, TCAddresses.CR0_W.value, Masks.BIT1_MASK.value
    )  # clear fault status register, only use with Interrupt Fault Mode


@unique
class DecBits4(Enum):
    """
    Valid decimal values for temperature registers with precision up to 2^-4.
    The MAX31856 uses a custom bit value scheme for setting temperature decimal values.
    One such scheme allocates 4 bits for this purpose, meaning only 16 decimal values are
    possible.

    These are listed below. Note, these values are not intended to be combined, as there
    is no guarantee the sum value can be represented. Please only select the exact value
    you need from this list.

    Examples:
        P0_5 represents the decimal value 0.5
        P0 represents the decimal value 0.0
        P0_0625 represents the decimal value 0.0625
    """

    P0 = 0b0000
    P0_5 = 0b1000
    P0_75 = 0b1100
    P0_875 = 0b1110
    P0_9375 = 0b1111
    P0_4375 = 0b0111
    P0_1875 = 0b0011
    P0_0625 = 0b0001
    P0_5625 = 0b1001
    P0_8125 = 0b1101
    P0_6875 = 0b1011
    P0_25 = 0b0100
    P0_125 = 0b0010
    P0_625 = 0b1010
    P0_3125 = 0b0101
    P0_375 = 0b0110


@unique
class DecBits6(Enum):
    """
    Valid decimal values for temperature registers with precision up to 2^-6.
    The MAX31856 uses a custom bit value scheme for setting temperature decimal values.
    One such scheme allocates 6 bits for this purpose, meaning only 64 decimal values are
    possible.

    These are listed below. Note, these values are not intended to be combined, as there
    is no guarantee the sum value can be represented. Please only select the exact value
    you need from this list.

    Examples:
        P0_5 represents the decimal value 0.5
        P0 represents the decimal value 0.0
        P0_0625 represents the decimal value 0.0625
    """

    P0 = 0b000000
    P0_015625 = 0b000001
    P0_03125 = 0b000010
    P0_046875 = 0b000011
    P0_0625 = 0b000100
    P0_078125 = 0b000101
    P0_09375 = 0b000110
    P0_109375 = 0b000111
    P0_125 = 0b001000
    P0_140625 = 0b001001
    P0_15625 = 0b001010
    P0_171875 = 0b001011
    P0_1875 = 0b001100
    P0_203125 = 0b001101
    P0_21875 = 0b001110
    P0_234375 = 0b001111
    P0_25 = 0b010000
    P0_265625 = 0b010001
    P0_28125 = 0b010010
    P0_296875 = 0b010011
    P0_3125 = 0b010100
    P0_328125 = 0b010101
    P0_34375 = 0b010110
    P0_359375 = 0b010111
    P0_375 = 0b011000
    P0_390625 = 0b011001
    P0_40625 = 0b011010
    P0_421875 = 0b011011
    P0_4375 = 0b011100
    P0_453125 = 0b011101
    P0_46875 = 0b011110
    P0_484375 = 0b011111
    P0_5 = 0b100000
    P0_515625 = 0b100001
    P0_53125 = 0b100010
    P0_546875 = 0b100011
    P0_5625 = 0b100100
    P0_578125 = 0b100101
    P0_59375 = 0b100110
    P0_609375 = 0b100111
    P0_625 = 0b101000
    P0_640625 = 0b101001
    P0_65625 = 0b101010
    P0_671875 = 0b101011
    P0_6875 = 0b101100
    P0_703125 = 0b101101
    P0_71875 = 0b101110
    P0_734375 = 0b101111
    P0_75 = 0b110000
    P0_765625 = 0b110001
    P0_78125 = 0b110010
    P0_796875 = 0b110011
    P0_8125 = 0b110100
    P0_828125 = 0b110101
    P0_84375 = 0b110110
    P0_859375 = 0b110111
    P0_875 = 0b111000
    P0_890625 = 0b111001
    P0_90625 = 0b111010
    P0_921875 = 0b111011
    P0_9375 = 0b111100
    P0_953125 = 0b111101
    P0_96875 = 0b111110
    P0_984375 = 0b111111


@unique
class ConvMode(Enum):
    """valid opcodes for setting thermocouple conversion mode"""

    SINGLE = OpCode(
        0x00, TCAddresses.CR0_W.value, Masks.BIT7_MASK.value
    )  # set thermocouple to perform single, manually triggered conversions
    AUTO = OpCode(
        0x80, TCAddresses.CR0_W.value, Masks.BIT7_MASK.value
    )  # set thermocouple to perform continuous conversions


@unique
class CJMode(Enum):
    """valid opcodes for setting thermocouple cold junction mode"""

    ENABLE = OpCode(
        0x00, TCAddresses.CR0_W.value, Masks.BIT3_MASK.value
    )  # enable the cold-junction sensor
    DISABLE = OpCode(
        0x08, TCAddresses.CR0_W.value, Masks.BIT3_MASK.value
    )  # disable the cold-junction sensor


@unique
class FaultMode(Enum):
    """valid opcodes for setting thermocouple fault mode"""

    COMPARATOR = OpCode(
        0x00, TCAddresses.CR0_W.value, Masks.BIT2_MASK.value
    )  # faults deassert only once fault condition is no longer true
    INTERRUPT = OpCode(
        0x04, TCAddresses.CR0_W.value, Masks.BIT2_MASK.value
    )  # faults deassert only once TCOps.CLEAR_FAULTS command is issued


@unique
class NoiseFilterMode(Enum):
    """valid opcodes for setting thermocouple noise rejection filter mode"""

    HZ_60 = OpCode(
        0x00, TCAddresses.CR0_W.value, Masks.BIT0_MASK.value
    )  # reject 60 Hz and its harmonics
    HZ_50 = OpCode(
        0x01, TCAddresses.CR0_W.value, Masks.BIT0_MASK.value
    )  # reject 50 Hz and its harmonics


@unique
class AvgMode(Enum):
    """valid opcodes for setting thermocouple conversion averaging mode"""

    AVG_1 = OpCode(0x00, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)  # single sample
    AVG_2 = OpCode(0x10, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)  # 2 samples averaged
    AVG_4 = OpCode(0x20, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)  # 4 samples averaged
    AVG_8 = OpCode(0x30, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)  # 8 samples averaged
    AVG_16 = OpCode(0x40, TCAddresses.CR1_W.value, Masks.CR1_HIGH_MASK.value)  # 16 samples averaged

    @staticmethod
    def get_avg_mode(reg_val: int):
        """
        get the sampling average mode config enum by checking register value passed
        Args:
            reg_val (int): masked register value passed
        Return:
            avg_mode (Eum): avg_mode Enum value
        """
        if reg_val == 0:
            avg_mode = AvgMode.AVG_1
        elif reg_val == 16:
            avg_mode = AvgMode.AVG_2
        elif reg_val == 32:
            avg_mode = AvgMode.AVG_4
        elif reg_val == 48:
            avg_mode = AvgMode.AVG_8
        elif reg_val == 64:
            avg_mode = AvgMode.AVG_16
        else:
            avg_mode = None
        return avg_mode

@unique
class TCType(Enum):
    """valid opcodes for setting thermocouple type"""

    TYPE_B = OpCode(0x00, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)  # type B thermocouple
    TYPE_E = OpCode(0x01, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)  # type E thermocouple
    TYPE_J = OpCode(0x02, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)  # type J thermocouple
    TYPE_K = OpCode(0x03, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)  # type K thermocouple
    TYPE_N = OpCode(0x04, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)  # type N thermocouple
    TYPE_R = OpCode(0x05, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)  # type R thermocouple
    TYPE_S = OpCode(0x06, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)  # type S thermocouple
    TYPE_T = OpCode(0x07, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value)  # type T thermocouple

    @staticmethod
    def get_tc_type(reg_val: int):
        """
        get the thermocouple type config enum by checking register value passed
        Args:
            reg_val (int): masked register value passed
        Return:
            tc_type (Eum): TC_type Enum value
        """
        if reg_val == 0:
            tc_type = TCType.TYPE_B
        elif reg_val == 1:
            tc_type = TCType.TYPE_E
        elif reg_val == 2:
            tc_type = TCType.TYPE_J
        elif reg_val == 3:
            tc_type = TCType.TYPE_K
        elif reg_val == 4:
            tc_type = TCType.TYPE_N
        elif reg_val == 5:
            tc_type = TCType.TYPE_R
        elif reg_val == 6:
            tc_type = TCType.TYPE_S
        elif reg_val == 7:
            tc_type = TCType.TYPE_T
        else:
            tc_type = None
        return tc_type

class VoltageMode(Enum):
    """
    valid opcodes for setting thermocouple voltage mode. Use to set
    thermocouple type other than those listed under TCType.
    Note, When voltage mode is selected, no linearization is
    performed on the conversion data. Use the voltage data
    and the cold-junction temperature to calculate the thermo-
    couple’s hot-junction temperature.
    """

    GAIN_8 = OpCode(
        0x08, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value
    )  # full-scale input voltage range of +/- 78.125 mV
    GAIN_32 = OpCode(
        0x0C, TCAddresses.CR1_W.value, Masks.CR1_LOW_MASK.value
    )  # full-scale input voltage range of +/- 19.531 mV


# Below are valid opcodes for setting the thermocouple fault mask register
# Example: OPEN_MASK_ON will 'mask' the OPEN fault from asserting through
# the FAULT pin, but the fault register will still be updated. OPEN_MASK_OFF
# will allow the OPEN fault to assert through the FAULT pin. Note, the FAULT
# pin is currently not connected on the EdgePi, so these settings do not currently
# result in any changes to the thermocouple functionality.
# Note, the MAX31856 does not permit unmasking the TCRANGE and CJRANGE faults.


@unique
class OpenMask(Enum):
    """valid opcodes for setting the thermocouple OPEN fault mask"""

    OPEN_MASK_ON = OpCode(0x01, TCAddresses.MASK_W.value, Masks.BIT0_MASK.value)
    OPEN_MASK_OFF = OpCode(0x00, TCAddresses.MASK_W.value, Masks.BIT0_MASK.value)


@unique
class OvuvMask(Enum):
    """valid opcodes for setting the thermocouple OVUV fault mask"""

    OVUV_MASK_ON = OpCode(0x02, TCAddresses.MASK_W.value, Masks.BIT1_MASK.value)
    OVUV_MASK_OFF = OpCode(0x00, TCAddresses.MASK_W.value, Masks.BIT1_MASK.value)


@unique
class TCLowMask(Enum):
    """valid opcodes for setting the thermocouple TCLOW fault mask"""

    TCLOW_MASK_ON = OpCode(0x04, TCAddresses.MASK_W.value, Masks.BIT2_MASK.value)
    TCLOW_MASK_OFF = OpCode(0x00, TCAddresses.MASK_W.value, Masks.BIT2_MASK.value)


@unique
class TCHighMask(Enum):
    """valid opcodes for setting the thermocouple TCHIGH fault mask"""

    TCHIGH_MASK_ON = OpCode(0x08, TCAddresses.MASK_W.value, Masks.BIT3_MASK.value)
    TCHIGH_MASK_OFF = OpCode(0x00, TCAddresses.MASK_W.value, Masks.BIT3_MASK.value)


@unique
class CJLowMask(Enum):
    """valid opcodes for setting the thermocouple CJLOW fault mask"""

    CJLOW_MASK_ON = OpCode(0x10, TCAddresses.MASK_W.value, Masks.BIT4_MASK.value)
    CJLOW_MASK_OFF = OpCode(0x00, TCAddresses.MASK_W.value, Masks.BIT4_MASK.value)


@unique
class CJHighMask(Enum):
    """valid opcodes for setting the thermocouple CJHIGH fault mask"""

    CJHIGH_MASK_ON = OpCode(0x20, TCAddresses.MASK_W.value, Masks.BIT5_MASK.value)
    CJHIGH_MASK_OFF = OpCode(0x00, TCAddresses.MASK_W.value, Masks.BIT5_MASK.value)


@unique
class OpenCircuitMode(Enum):
    """valid opcodes for setting thermocouple open circuit fault detection mode"""

    DISABLED = OpCode(0x00, TCAddresses.CR0_W.value, Masks.CR0_OC_MASK.value)
    LOW_INPUT_IMPEDANCE = OpCode(0x10, TCAddresses.CR0_W.value, Masks.CR0_OC_MASK.value)
    MED_INPUT_IMPEDANCE = OpCode(0x20, TCAddresses.CR0_W.value, Masks.CR0_OC_MASK.value)
    HIGH_INPUT_IMPEDANCE = OpCode(0x30, TCAddresses.CR0_W.value, Masks.CR0_OC_MASK.value)
