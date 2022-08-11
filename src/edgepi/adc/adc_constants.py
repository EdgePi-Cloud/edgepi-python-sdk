""" Constants for ADC device modules """


from dataclasses import dataclass
from enum import Enum, unique


@unique
class ADCOp(Enum):
    """EdgePi ADC operation codes"""

    OP_NOP = 0x00
    OP_RESET = 0x06
    OP_START1 = 0x09
    OP_STOP1 = 0x0A
    OP_START2 = 0x0C
    OP_STOP2 = 0x0E
    OP_RDATA1 = 0x12
    OP_RDATA2 = 0x14
    OP_SYOCAL1 = 0x16
    OP_SYGCAL1 = 0x17
    OP_SFOCAL1 = 0x19
    OP_SYOCAL2 = 0x1B
    OP_SYGCAL2 = 0x1C
    OP_SFOCAL2 = 0x1E
    OP_RREG = 0x20
    OP_WREG = 0x40


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
    """EdgePi ADC channels"""

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

class ADCNum(Enum):
    ''' ADS1263 ADC's '''
    ADC_1 = 1
    ADC_2 = 2

class ConvMode(Enum):
    '''
    ADS1263 conversion modes

    Attributes:

        `PULSE`: ADC1 performs a single conversion upon command

        `CONTINUOUS`: ADC1 peforms conversions continuously
    '''

class ADC1DataRate(Enum):
    """ ADS1263 data rates for ADC1 """

class ADC2DataRate(Enum):
    """ ADS1263 data rates for ADC2 """

class FilterMode(Enum):
    """ ADC filter modes, for both ADC1 and ADC2 """

class ADCAlarmTypes(Enum):
    """ ADC1 alarm types """

@dataclass
class ADCAlarm():
    """
    Represents information about the status of ADC1 alarm
    as indicated by a reading of the STATUS byte.
    """
    alarm_type: ADCAlarmTypes
    at_fault: bool
    err_msg: str
