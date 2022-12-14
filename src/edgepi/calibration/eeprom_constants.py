'''Address map of eeprom'''

from enum import Enum
from dataclasses import dataclass
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout
from edgepi.calibration.calibration_constants import CalibParam

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

@dataclass
class Keys:
    """
    Dataclass to store key strings
    """
    certificate: str = None
    private: str = None

@dataclass
class EdgePiEEPROMData:
    # pylint: disable=too-many-instance-attributes
    """
    Dataclass to store edgepi reserved values
    dac_calib_parms (dict): list of calibration parameters
    adc_calib_parms (dict): list of calibration parameters
    rtd_calib_parms (dict): list of calibration parameters
    tc_calib_parms (dict): list of calibration parameters
    config_key (Keys): dataclass
    data_key (Keys): dataclass
    serial (str)
    model (str)
    client_id (str)
    """
    dac_calib_parms: dict = None
    adc_calib_parms: dict = None
    rtd_calib_parms: dict = None
    tc_calib_parms: dict = None
    config_key: Keys = None
    data_key: Keys = None
    serial: str = None
    model: str = None
    client_id: str = None

    def message_to_dict(self, data_to_unpack: EepromLayout = None):
        """
        Function to unpack message to list
        Args:
            data_to_unpack: EepromLayout message modules
        Returns:
            calib_list: 1-D array
        """
        calib_dict={}
        for indx, ch in enumerate(data_to_unpack.calibs):
            calib_dict[indx] = CalibParam(gain=ch.gain,
                                        offset=ch.offset)
        return calib_dict

    def keys_to_str(self, data_to_unpack: EepromLayout = None):
        """
        Function to unpack message to string
        Args:
            data_to_unpack: EepromLayout message keys
        Returns:
            Keys (dataclass): keys values
        """
        return Keys(certificate = data_to_unpack.certificate, private = data_to_unpack.private_key)
