'''Address map of eeprom'''

from enum import Enum

class EEPROMInfo(Enum):
    """
    EEPROM device address for I2C addressing
    """
    DEV_ADDR = 0x50
    PAGE_SIZE = 64
    NUM_OF_PAGE = 512

class ModuleNames(Enum):
    """
    Module Name Enum
    """
    DAC = 0x0
    ADC = 0x1
    RTD = 0x2
    TC = 0x3

class EdgePiMemoryInfo(Enum):
    """
    Information regarding Edgepi reserved memory space
    """
    USED_SPACE = 0x00
    BUFF_START = 0x02

    PRIVATE_SPACE_START_BYTE = 0x0
    PRIVATE_SPACE_END_BYTE = 0x3FFF
    PRIVATE_SPACE_START_PAGE = 0x0
    PRIVATE_SPACE_END_PAGE = 0x0FF

    USER_SPACE_START_BYTE = 0x4000
    USER_SPACE_END_BYTE = 0x7FFF
    USER_SPACE_START_PAGE = 0x100
    USER_SPACE_END_PAGE = 0x1FF
    USER_SPACE_MAX = 0X3FFC

    FACTORY_DEFAULT_VALUE = 0xFFFF

class MessageFieldNumber(Enum):
    """
    MessageField index number to be used for ListFields() function. The function lists fields start
    from index 0
    """
    DAC=1
    ADC=2
    RTD=3
    TC=4
    CONFIGS_KEY=5
    DATA_KEY=6
    SERIAL=7
    MODEL=8
    CLIENT_ID=9
    ALL=10

