"""module to map protobuf data to a class"""

# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372
from dataclasses import dataclass
from edgepi.eeprom.eeprom_mapping_pb2 import EepromLayout
from edgepi.calibration.calibration_constants import CalibParam

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
    client_id_config (str)
    client_id_data (str)
    thing_id (str)
    """

    def __init__(self, data_to_unpack: EepromLayout = None):
        self.dac_calib_params = self.calib_message_to_dict(data_to_unpack.dac)
        self.adc_calib_params = self.calib_message_to_dict(data_to_unpack.adc)
        self.rtd_calib_params = self.calib_message_to_dict(data_to_unpack.rtd)
        self.rtd_hw_params = self.hw_message_to_dict(data_to_unpack.rtd)
        self.tc_calib_params = self.calib_message_to_dict(data_to_unpack.tc)
        self.tc_hw_params = self.hw_message_to_dict(data_to_unpack.tc)
        self.config_key = self.keys_to_dataclass(data_to_unpack.config_key)
        self.data_key = self.keys_to_dataclass(data_to_unpack.data_key)
        self.serial = data_to_unpack.serial_number
        self.model = data_to_unpack.model
        self.client_id_config = data_to_unpack.client_id_config
        self.client_id_data = data_to_unpack.client_id_data
        self.thing_id = data_to_unpack.thing_id

    def calib_message_to_dict(self, data_to_unpack: EepromLayout = None):
        """
        Function to unpack message to list
        Args:
            data_to_unpack: EepromLayout message modules
        Returns:
            calib_dict: calib param to dictionary
        """
        calib_dict={}
        for indx, ch in enumerate(data_to_unpack.calibs):
            calib_dict[indx] = CalibParam(gain=ch.gain,
                                        offset=ch.offset)
        return calib_dict

    def hw_message_to_dict(self, data_to_unpack: EepromLayout = None):
        """
        Function to unpack message to list
        Args:
            data_to_unpack: EepromLayout message modules
        Returns:
            hw_params: hardware param to dictionary
        """
        hw_dict={}
        for indx, ch in enumerate(data_to_unpack.hw_val):
            hw_dict[indx] = ch.ref_resistor
        return hw_dict

    def keys_to_dataclass(self, data_to_unpack: EepromLayout = None):
        """
        Function to unpack message and populate into Keys dataclass in string format
        Args:
            data_to_unpack: EepromLayout message keys
        Returns:
            Keys (dataclass): keys values
        """
        return Keys(certificate = data_to_unpack.certificate, private = data_to_unpack.private_key)

    def pack_dac_calib(self, proto_buf: EepromLayout):
        """
        Pack dac calib dictionary to proto_buf messages
        Args:
            proto_buf (EepromLayout): proto_buf dac message
        """
        for ch, calib_param in self.dac_calib_params.items():
            proto_buf.calibs[ch].gain = calib_param.gain
            proto_buf.calibs[ch].offset = calib_param.offset

    def pack_adc_calib(self, proto_buf: EepromLayout):
        """
        Pack adc calib dictionary to proto_buf messages
        Args:
            proto_buf (EepromLayout): proto_buf adc message
        """
        for ch, calib_param in self.adc_calib_params.items():
            proto_buf.calibs[ch].gain = calib_param.gain
            proto_buf.calibs[ch].offset = calib_param.offset

    def pack_rtd_calib(self, proto_buf: EepromLayout):
        """
        Pack rtd calib dictionary to proto_buf messages
        Args:
            proto_buf (EepromLayout): proto_buf rtd message
        """
        for ch, calib_param in self.rtd_calib_params.items():
            proto_buf.calibs[ch].gain = calib_param.gain
            proto_buf.calibs[ch].offset = calib_param.offset

    def pack_rtd_hw(self, proto_buf: EepromLayout):
        """
        Pack rtd hardware dictionary to pb messages
        Args:
            proto_buf (EepromLayout): proto_buf rtd message
        """
        for indx, hw_param in self.rtd_hw_params.items():
            proto_buf.hw_val[indx].ref_resistor = hw_param

    def pack_tc_calib(self, proto_buf: EepromLayout):
        """
        Pack tc calib dictionary to proto_buf messages
        Args:
            proto_buf (EepromLayout): proto_buf tc message
        """
        for ch, calib_param in self.tc_calib_params.items():
            proto_buf.calibs[ch].gain = calib_param.gain
            proto_buf.calibs[ch].offset = calib_param.offset

    def pack_tc_hw(self, proto_buf: EepromLayout):
        """
        Pack tc hardware dictionary to proto_buf messages
        Args:
            proto_buf (EepromLayout): proto_buf tc message
        """
        for indx, hw_param in self.tc_hw_params.items():
            proto_buf.hw_val[indx].ref_resistor = hw_param

    def pack_config_key(self, proto_buf: EepromLayout):
        """
        Pack config key dataclass to proto_buf
        Args:
            proto_buf (EepromLayout): proto_buf config_key message
        """
        proto_buf.certificate = self.config_key.certificate
        proto_buf.private_key = self.config_key.private

    def pack_data_key(self, proto_buf: EepromLayout):
        """
        Pack data key dataclass to proto_buf
        Args:
            proto_buf (EepromLayout): proto_buf data key message
        """
        proto_buf.certificate = self.data_key.certificate
        proto_buf.private_key = self.data_key.private

    def pack_product_info(self, proto_buf: EepromLayout):
        """
        Pack product data
        Args:
            proto_buf (EepromLayout): proto_buf data
        """
        proto_buf.serial_number = self.serial
        proto_buf.model = self.model
        proto_buf.client_id_config = self.client_id_config
        proto_buf.client_id_data = self.client_id_data
        proto_buf.thing_id = self.thing_id

    def pack_dataclass(self, proto_buf: EepromLayout):
        """
        Function to populate current dictionary value to proto buffer message
        Args:
            proto_buf (EepromLayout): protobuffer layout
        # """
        self.pack_dac_calib(proto_buf.dac)
        self.pack_adc_calib(proto_buf.adc)
        self.pack_rtd_calib(proto_buf.rtd)
        self.pack_rtd_hw(proto_buf.rtd)
        self.pack_tc_calib(proto_buf.tc)
        self.pack_tc_hw(proto_buf.tc)
        self.pack_config_key(proto_buf.config_key)
        self.pack_data_key(proto_buf.data_key)
        self.pack_product_info(proto_buf)
