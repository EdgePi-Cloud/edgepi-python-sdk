'''Address map of eeprom'''

from enum import Enum

# page write cycle time requirements https://www.onsemi.com/pdf/datasheet/cat24c256-d.pdf
PAGE_WRITE_CYCLE_TIME=0.01
DEFAULT_EEPROM_BIN_B64 = b"CmAKCg0AAIA/FQAAAAASCg0AAIA/FQAAAAAaCg0AAIA/FQAAAAAiCg0AAIA/FQAAAAAqCg0A\
                       AIA/FQAAAAAyCg0AAIA/FQAAAAA6Cg0AAIA/FQAAAABCCg0AAIA/FQAAAAASkAEKCg0AAIA/FQAA\
                       AAASCg0AAIA/FQAAAAAaCg0AAIA/FQAAAAAiCg0AAIA/FQAAAAAqCg0AAIA/FQAAAAAyCg0AAIA/\
                       FQAAAAA6Cg0AAIA/FQAAAABCCg0AAIA/FQAAAABKCg0AAIA/FQAAAABSCg0AAIA/FQAAAABaCg0A\
                       AIA/FQAAAABiCg0AAIA/FQAAAAAakAEKCg0AAIA/FQAAAAASCg0AAIA/FQAAAAAaCg0AAIA/FQAA\
                       AAAiCg0AAIA/FQAAAAAqCg0AAIA/FQAAAAAyCg0AAIA/FQAAAAA6Cg0AAIA/FQAAAABCCg0AAIA/\
                       FQAAAABKCg0AAIA/FQAAAABSCg0AAIA/FQAAAABaCg0AAIA/FQAAAABiCg0AAIA/FQAAAAAiEQoK\
                       DQAAgD8VAAAAABUAAPpEKmAKCg0AAIA/FQAAAAASCg0AAIA/FQAAAAAaCg0AAIA/FQAAAAAiCg0A\
                       AIA/FQAAAAAqCg0AAIA/FQAAAAAyCg0AAIA/FQAAAAA6Cg0AAIA/FQAAAABCCg0AAIA/FQAAAAAy\
                       NAoWVGhpcyBpcyBDb25maWcgUHJpdmF0ZRIaVGhpcyBpcyBDb25maWcgQ2VydGlmaWNhdGU6MAoU\
                       VGhpcyBpcyBEYXRhIFByaXZhdGUSGFRoaXMgaXMgRGF0YSBDZXJ0aWZpY2F0ZUIVVGhpcyBpcyBT\
                       ZXJpYWwgTnVtYmVyShxUaGlzIGlzIGNtIGJvYXJkIHBhcnQgbnVtYmVyUhZUaGlzIGlzIHRiIHBh\
                       cnQgbnVtYmVyWhdUaGlzIGlzIGNtNCBwYXJ0IG51bWJlcmIUVGhpcyBpcyBNb2RlbCBOdW1iZXI="

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

class EepromModuleNames(Enum):
    """
    MessageField index number to be used for ListFields() function. The function lists fields start
    from index 0
    """
    DAC_CALIB_PARAMS="dac_calib_params"
    ADC1_CALIB_PARAMS="adc1_calib_params"
    ADC2_CALIB_PARAMS="adc2_calib_params"
    RTD_CALIB_PARAMS="rtd_calib_params"
    TC_CALIB_PARAMS="tc_calib_params"
    CONFIG_KEY="config_key"
    DATA_KEY="data_key"
    SERIAL="serial"
    MODEL="model"
    CM_PART_NUMBER="cm_part_number"
    TB_PART_NUMBER="tb_part_number"
    CM4_PART_NUMBER="cm4_part_number"
