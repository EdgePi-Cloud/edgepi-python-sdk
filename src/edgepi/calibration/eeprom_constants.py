'''Address map of eeprom'''

from enum import Enum

class EEPROMAddress(Enum):
    """
    EEPROM device address for I2C addressing
    """
    DEV_ADDR = 0x50

class ModuleNames(Enum):
    """
    Module Name Enum
    """
    DAC = 0x0
    ADC = 0x1
    RTD = 0x2
    TC = 0x3

class DACParamAddr(Enum):
    """
    EdgePi DAC Calibration Parameter Addresses
    Each parameter, gain and offset, are 4 bytes long 0x200~0x23F
    Ex) CH0_gain = 0x200~0x203, CH0_offset = 0x204~0x207
    """

    CH0 = 0x200
    CH1 = 0x208
    CH2 = 0x210
    CH3 = 0x218
    CH4 = 0x220
    CH5 = 0x228
    CH6 = 0x230
    CH7 = 0x238
    LEN = 63

class ADCParamAddr(Enum):
    """
    EdgePi DAC Calibration Parameter Addresses
    Each parameter, gain and offset, are 4 bytes long
    """

    CH0 = 0x240
    CH1 = 0x248
    CH2 = 0x240
    CH3 = 0x248
    CH4 = 0x240
    CH5 = 0x248
    CH6 = 0x240
    CH7 = 0x248
    DIFF1 =0x250
    DIFF2 =0x258
    DIFF3 =0x260
    DIFF4 =0x268

class MemoryAddr(Enum):
    """
    Memory offset values
    """
    START = 0x000
    DAC = 0x200
    ADC = 0x240
    TC = 0x280
    RTD = 0x2C0
    END = 0x3FF
    CH_OFFSET = 0x8
