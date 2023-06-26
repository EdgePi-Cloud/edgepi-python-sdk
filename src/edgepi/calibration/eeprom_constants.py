'''Address map of eeprom'''

from enum import Enum

# page write cycle time requirements https://www.onsemi.com/pdf/datasheet/cat24c256-d.pdf
PAGE_WRITE_CYCLE_TIME=0.01
DEFUALT_EEPROM_BIN = b"CmAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/\
                       FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAASkAEKCg0AAIA/FQAAAAAK\
                       Cg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAA\
                       AAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/FQAAAAAKCg0AAIA/\
                       FQAAAAAKCg0AAIA/FQAAAAAaEwoKDQAAgD8VAAAAABIFDQAAgD8iEwoKDQAAgD8VAAAAABIFDQAA\
                       gD8qJAoOQ29uZmlnLVByaXZhdGUSEkNvbmZpZy1DZXJ0aWZpY2F0ZTIgCgxEYXRhLXByaXZhdGUS\
                       EERhdGEtY2VydGlmaWNhdGU6DDIwMjIxMTEwLTAyMUIPRWRnZVBpLUJlYXJib25lSgxTTy0yMDIy\
                       LTEwMjM="

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
