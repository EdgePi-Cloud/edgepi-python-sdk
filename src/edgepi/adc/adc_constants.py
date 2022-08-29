""" Constants for ADC device modules """


from dataclasses import dataclass
from enum import Enum, unique

from edgepi.reg_helper.reg_helper import BitMask, OpCode


ADC_NUM_REGS = 27


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
    FLOAT = 0xF


@dataclass
class ADCReadInfo:
    """
    Data for use in performing ADC voltage reads

    Attributes:
        id_num (int): the ADS1263 ID number of this ADC
        addx (ADCChannel): addx of this ADC's mux register
        num_data_bytes (int): number of data bytes for this ADC's reads
        start_cmd (ADCComs): command to trigger conversion(s) for this ADC
        read_cmd (ADCComs): command to read this ADC's data-holding register
        stop_cmd (ADCComs): command to stop conversion(s) for this ADC
    """

    id_num: int
    addx: ADCChannel
    num_data_bytes: int
    start_cmd: ADCComs
    read_cmd: ADCComs
    stop_cmd: ADCComs


class ADCNum(Enum):
    """ADS1263 ADC's"""

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


class ADC2DataRate(Enum):
    """ADS1263 data rates for ADC2"""


class FilterMode(Enum):
    """ADC filter modes, for both ADC1 and ADC2"""


class ADCAlarmTypes(Enum):
    """ADC1 alarm types"""


@dataclass
class ADCAlarm:
    """
    Represents information about the status of ADC1 alarm
    as indicated by a reading of the STATUS byte.
    """

    alarm_type: ADCAlarmTypes
    at_fault: bool
    err_msg: str
