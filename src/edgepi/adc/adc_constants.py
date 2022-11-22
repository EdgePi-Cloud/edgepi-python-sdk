""" Constants for ADC device modules """


from dataclasses import dataclass
from enum import Enum, unique

from edgepi.reg_helper.reg_helper import BitMask, OpCode


ADC_NUM_REGS = 27  # number of ADC1263 registers
ADC_VOLTAGE_READ_LEN = 6  # number of bytes per voltage read


@unique
class ADCComs(Enum):
    """EdgePi ADC operation codes"""

    COM_NOP = 0x00
    COM_RESET = 0x06
    COM_START1 = 0x09
    COM_STOP1 = 0x0A
    COM_START2 = 0x0C
    COM_STOP2 = 0x0E
    COM_RDATA1 = 0x12
    COM_RDATA2 = 0x14
    COM_SYOCAL1 = 0x16
    COM_SYGCAL1 = 0x17
    COM_SFOCAL1 = 0x19
    COM_SYOCAL2 = 0x1B
    COM_SYGCAL2 = 0x1C
    COM_SFOCAL2 = 0x1E
    COM_RREG = 0x20
    COM_WREG = 0x40


@unique
class ADCReg(Enum):
    """EdgePi ADC register addresses"""

    REG_ID = 0x00
    REG_POWER = 0x01
    REG_INTERFACE = 0x02
    REG_MODE0 = 0x03
    REG_MODE1 = 0x04
    REG_MODE2 = 0x05
    REG_INPMUX = 0x06
    REG_OFCAL0 = 0x07
    REG_OFCAL1 = 0x08
    REG_OFCAL2 = 0x09
    REG_FSCAL0 = 0x0A
    REG_FSCAL1 = 0x0B
    REG_FSCAL2 = 0x0C
    REG_IDACMUX = 0x0D
    REG_IDACMAG = 0x0E
    REG_REFMUX = 0x0F
    REG_TDACP = 0x10
    REG_TDACN = 0x11
    REG_GPIOCON = 0x12
    REG_GPIODIR = 0x13
    REG_GPIODAT = 0x14
    REG_ADC2CFG = 0x15
    REG_ADC2MUX = 0x16
    REG_ADC2OFC0 = 0x17
    REG_ADC2OFC1 = 0x18
    REG_ADC2FSC0 = 0x19
    REG_ADC2FSC1 = 0x1A


@unique
class ADCChannel(Enum):
    """EdgePi ADC channels/channel modes"""

    AIN0 = 0
    AIN1 = 1
    AIN2 = 2
    AIN3 = 3
    AIN4 = 4
    AIN5 = 5
    AIN6 = 6
    AIN7 = 7
    AIN8 = 8
    AIN9 = 9
    AINCOM = 10
    FLOAT = 0xF


@dataclass(frozen=True)
class ADCReadInfo:
    """
    Data for use in performing ADC voltage reads

    Attributes:
        `id_num` (int): the ADS1263 ID number of this ADC
        `addx` (ADCReg): addx of this ADC's mux register
        `num_data_bytes` (int): number of data bytes for this ADC's reads
        `start_cmd` (ADCComs): command to trigger conversion(s) for this ADC
        `read_cmd` (ADCComs): command to read this ADC's data-holding register
        `stop_cmd` (ADCComs): command to stop conversion(s) for this ADC
    """

    id_num: int
    addx: ADCReg
    num_data_bytes: int
    start_cmd: ADCComs
    read_cmd: ADCComs
    stop_cmd: ADCComs


# TODO: use EEPROM values in ADCVoltageConfig
# TODO: refactor voltage configs from per ADC to per channel
@unique
class ADCNum(Enum):
    """ADS1263 ADCs"""

    ADC_1 = ADCReadInfo(
        1,
        ADCReg.REG_INPMUX,
        4,
        ADCComs.COM_START1.value,
        ADCComs.COM_RDATA1.value,
        ADCComs.COM_STOP1.value,
    )
    ADC_2 = ADCReadInfo(
        2,
        ADCReg.REG_ADC2MUX,
        3,
        ADCComs.COM_START2.value,
        ADCComs.COM_RDATA2.value,
        ADCComs.COM_STOP2.value,
    )


class ConvMode(Enum):
    """
    ADS1263 conversion modes for ADC1

    Attributes:

        `PULSE`: ADC1 performs a single conversion upon command

        `CONTINUOUS`: ADC1 peforms conversions continuously
    """

    CONTINUOUS = OpCode(0x00, ADCReg.REG_MODE0.value, BitMask.BIT6.value)
    PULSE = OpCode(0x40, ADCReg.REG_MODE0.value, BitMask.BIT6.value)


class ADC1DataRate(Enum):
    """ADS1263 data rates for ADC1"""

    SPS_2P5 = OpCode(0x0, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_5 = OpCode(0x1, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_10 = OpCode(0x2, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_16P6 = OpCode(0x3, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_20 = OpCode(0x4, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_50 = OpCode(0x5, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_60 = OpCode(0x6, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_100 = OpCode(0x7, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_400 = OpCode(0x8, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_1200 = OpCode(0x9, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_2400 = OpCode(0xA, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_4800 = OpCode(0xB, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_7200 = OpCode(0xC, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_14400 = OpCode(0xD, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_19200 = OpCode(0xE, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)
    SPS_38400 = OpCode(0xF, ADCReg.REG_MODE2.value, BitMask.LOW_NIBBLE.value)


class ADCMasks(Enum):
    """ADS1263 OpCode bit masks"""

    FILTER_BITS = 0x1F  # overwrite bits 7:5 (0-indexed)
    CHECK_BITS = 0xFC  # overwrite bits 1:0
    ADC2_DR_BITS = 0x3F  # overwrite bits 7:6
    RMUXP_BITS = 0xC7  # overwrite bits 5:3
    RMUXN_BITS = 0xF8  # overwrite bits 2:0


class ADC2DataRate(Enum):
    """ADS1263 data rates for ADC2"""

    SPS_10 = OpCode(0x00, ADCReg.REG_ADC2CFG.value, ADCMasks.ADC2_DR_BITS.value)
    SPS_100 = OpCode(0x40, ADCReg.REG_ADC2CFG.value, ADCMasks.ADC2_DR_BITS.value)
    SPS_400 = OpCode(0x80, ADCReg.REG_ADC2CFG.value, ADCMasks.ADC2_DR_BITS.value)
    SPS_800 = OpCode(0xC0, ADCReg.REG_ADC2CFG.value, ADCMasks.ADC2_DR_BITS.value)


class FilterMode(Enum):
    """ADC filter modes, for both ADC1 and ADC2"""

    SINC1 = OpCode(0x0, ADCReg.REG_MODE1.value, ADCMasks.FILTER_BITS.value)
    SINC2 = OpCode(0x20, ADCReg.REG_MODE1.value, ADCMasks.FILTER_BITS.value)
    SINC3 = OpCode(0x40, ADCReg.REG_MODE1.value, ADCMasks.FILTER_BITS.value)
    SINC4 = OpCode(0x60, ADCReg.REG_MODE1.value, ADCMasks.FILTER_BITS.value)
    FIR = OpCode(0x80, ADCReg.REG_MODE1.value, ADCMasks.FILTER_BITS.value)


class ADCReferenceSwitching(Enum):
    """Each ADC Reference ground can be configured"""

    GND_SW_NONE = 0
    GND_SW1 = 1
    GND_SW2 = 2
    GND_SW_BOTH = 3


class ADCPower(Enum):
    """OpCodes for configuring the ADS1263 POWER register"""

    RESET_CLEAR = OpCode(0x0, ADCReg.REG_POWER.value, BitMask.BIT4.value)


class CheckMode(Enum):
    """OpCodes for configuring ADS1263 voltage read check mode"""

    CHECK_BYTE_OFF = OpCode(0x00, ADCReg.REG_INTERFACE.value, ADCMasks.CHECK_BITS.value)
    CHECK_BYTE_CHK = OpCode(0x01, ADCReg.REG_INTERFACE.value, ADCMasks.CHECK_BITS.value)
    CHECK_BYTE_CRC = OpCode(0x02, ADCReg.REG_INTERFACE.value, ADCMasks.CHECK_BITS.value)


class StatusByte(Enum):
    """OpCodes for configuring ADS1263 voltage read status byte"""

    STATUS_BYTE_ON = OpCode(0x04, ADCReg.REG_INTERFACE.value, BitMask.BIT2.value)
    STATUS_BYTE_OFF = OpCode(0x00, ADCReg.REG_INTERFACE.value, BitMask.BIT2.value)


@dataclass(frozen=True)
class DifferentialPair:
    """ADC differential voltage reading channel pairs"""

    mux_p: ADCChannel
    mux_n: ADCChannel


class DiffMode(Enum):
    """ADC differential voltage reading modes"""

    DIFF_1 = DifferentialPair(ADCChannel.AIN0, ADCChannel.AIN1)
    DIFF_2 = DifferentialPair(ADCChannel.AIN2, ADCChannel.AIN3)
    DIFF_3 = DifferentialPair(ADCChannel.AIN4, ADCChannel.AIN5)
    DIFF_4 = DifferentialPair(ADCChannel.AIN6, ADCChannel.AIN7)
    DIFF_OFF = DifferentialPair(ADCChannel.FLOAT, ADCChannel.AINCOM)


class IDACMUX(Enum):
    """Settings for ADC IDACMUX register (output multiplexer mapping)"""

    IDAC2_AIN0 = OpCode(0x0, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN1 = OpCode(0x10, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN2 = OpCode(0x20, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN3 = OpCode(0x30, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN4 = OpCode(0x40, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN5 = OpCode(0x50, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN6 = OpCode(0x60, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN7 = OpCode(0x70, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN8 = OpCode(0x80, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AIN9 = OpCode(0x90, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_AINCOM = OpCode(0xA0, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_NO_CONNECT = OpCode(0xB0, ADCReg.REG_IDACMUX.value, BitMask.HIGH_NIBBLE.value)
    IDAC1_AIN0 = OpCode(0x0, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN1 = OpCode(0x1, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN2 = OpCode(0x2, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN3 = OpCode(0x3, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN4 = OpCode(0x4, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN5 = OpCode(0x5, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN6 = OpCode(0x6, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN7 = OpCode(0x7, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN8 = OpCode(0x8, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AIN9 = OpCode(0x9, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_AINCOM = OpCode(0xA, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)
    IDAC1_NO_CONNECT = OpCode(0xB, ADCReg.REG_IDACMUX.value, BitMask.LOW_NIBBLE.value)


class IDACMAG(Enum):
    """Settings for ADC IDACMAG register (IDAC current magnitude in µA)"""

    IDAC2_OFF = OpCode(0x0, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_50 = OpCode(0x10, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_100 = OpCode(0x20, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_250 = OpCode(0x30, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_500 = OpCode(0x40, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_750 = OpCode(0x50, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_1000 = OpCode(0x60, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_1500 = OpCode(0x70, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_2000 = OpCode(0x80, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_2500 = OpCode(0x90, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC2_3000 = OpCode(0xA0, ADCReg.REG_IDACMAG.value, BitMask.HIGH_NIBBLE.value)
    IDAC1_OFF = OpCode(0x0, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_50 = OpCode(0x1, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_100 = OpCode(0x2, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_250 = OpCode(0x3, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_500 = OpCode(0x4, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_750 = OpCode(0x5, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_1000 = OpCode(0x6, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_1500 = OpCode(0x7, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_2000 = OpCode(0x8, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_2500 = OpCode(0x9, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)
    IDAC1_3000 = OpCode(0xA, ADCReg.REG_IDACMAG.value, BitMask.LOW_NIBBLE.value)


class REFMUX(Enum):
    """Settings for ADC REFMUX register (Reference multiplexer mapping)"""

    POS_REF_INT_2P5 = OpCode(0x0, ADCReg.REG_REFMUX.value, ADCMasks.RMUXP_BITS.value)
    POS_REF_EXT_AIN0 = OpCode(0x8, ADCReg.REG_REFMUX.value, ADCMasks.RMUXP_BITS.value)
    POS_REF_EXT_AIN2 = OpCode(0x10, ADCReg.REG_REFMUX.value, ADCMasks.RMUXP_BITS.value)
    POS_REF_EXT_AIN4 = OpCode(0x18, ADCReg.REG_REFMUX.value, ADCMasks.RMUXP_BITS.value)
    POS_REF_INT_VAVDD = OpCode(0x20, ADCReg.REG_REFMUX.value, ADCMasks.RMUXP_BITS.value)
    NEG_REF_INT_2P5 = OpCode(0x0, ADCReg.REG_REFMUX.value, ADCMasks.RMUXN_BITS.value)
    NEG_REF_EXT_AIN1 = OpCode(0x1, ADCReg.REG_REFMUX.value, ADCMasks.RMUXN_BITS.value)
    NEG_REF_EXT_AIN3 = OpCode(0x2, ADCReg.REG_REFMUX.value, ADCMasks.RMUXN_BITS.value)
    NEG_REF_EXT_AIN5 = OpCode(0x3, ADCReg.REG_REFMUX.value, ADCMasks.RMUXN_BITS.value)
    NEG_REF_INT_VAVSS = OpCode(0x4, ADCReg.REG_REFMUX.value, ADCMasks.RMUXN_BITS.value)


class RTDModes(Enum):
    "ADC.__config args for for turning RTD mode on/off"
    RTD_ON = {
        "adc_1_analog_in": ADCChannel.AIN5,
        "adc_1_mux_n": ADCChannel.AIN6,
        "idac_1_mux": IDACMUX.IDAC1_AIN8,
        "idac_2_mux": IDACMUX.IDAC2_AIN9,
        "idac_1_mag": IDACMAG.IDAC1_500,
        "idac_2_mag": IDACMAG.IDAC2_500,
        "pos_ref_inp": REFMUX.POS_REF_EXT_AIN4,
        "neg_ref_inp": REFMUX.NEG_REF_INT_VAVSS,
    }
    RTD_OFF = {
        "adc_1_analog_in": ADCChannel.FLOAT,
        "adc_1_mux_n": ADCChannel.AINCOM,
        "idac_1_mux": IDACMUX.IDAC1_NO_CONNECT,
        "idac_2_mux": IDACMUX.IDAC2_NO_CONNECT,
        "idac_1_mag": IDACMAG.IDAC1_OFF,
        "idac_2_mag": IDACMAG.IDAC2_OFF,
        "pos_ref_inp": REFMUX.POS_REF_INT_2P5,
        "neg_ref_inp": REFMUX.NEG_REF_INT_2P5,
    }


class AllowedChannels(Enum):
    """Available channels for reading depend on whether RTD is enabled or not"""

    RTD_ON = [
        ADCChannel.AIN0,
        ADCChannel.AIN1,
        ADCChannel.AIN2,
        ADCChannel.AIN3,
        ADCChannel.AIN7,
        ADCChannel.AINCOM,
        ADCChannel.FLOAT,
    ]
    RTD_OFF = [
        ADCChannel.AIN0,
        ADCChannel.AIN1,
        ADCChannel.AIN2,
        ADCChannel.AIN3,
        ADCChannel.AIN4,
        ADCChannel.AIN5,
        ADCChannel.AIN6,
        ADCChannel.AIN7,
        ADCChannel.AINCOM,
        ADCChannel.FLOAT,
    ]
