"""module to map protobuf data to a class"""

from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout
from edgepi.calibration.calibration_constants import CalibParam
from dataclasses import dataclass

@dataclass
class Keys:
    """
    Dataclass to store key strings
    """
    certificate: str = None
    private: str = None


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
    def __init__(self, data_to_unpack: EepromLayout = None):
        self.dac_calib_parms = self.message_to_dict(data_to_unpack.dac)
        self.adc_calib_parms = self.message_to_dict(data_to_unpack.dac)
        self.rtd_calib_parms = self.message_to_dict(data_to_unpack.dac)
        self.tc_calib_parms = self.message_to_dict(data_to_unpack.dac)
        self.config_key = self.keys_to_dataclass(data_to_unpack.config_key)
        self.data_key = self.keys_to_dataclass(data_to_unpack.data_key)
        self.serial = data_to_unpack.serial_number
        self.model = data_to_unpack.model
        self.client_id = data_to_unpack.client_id

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

    def keys_to_dataclass(self, data_to_unpack: EepromLayout = None):
        """
        Function to unpack message and populate into Keys dataclass in string format
        Args:
            data_to_unpack: EepromLayout message keys
        Returns:
            Keys (dataclass): keys values
        """
        return Keys(certificate = data_to_unpack.certificate, private = data_to_unpack.private_key)
