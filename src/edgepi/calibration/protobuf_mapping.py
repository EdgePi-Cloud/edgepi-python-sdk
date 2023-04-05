"""module to map protobuf data to a class"""

# pylint: disable=no-name-in-module
# https://github.com/protocolbuffers/protobuf/issues/10372
from dataclasses import dataclass
from edgepi.calibration.eeprom_constants import MessageFieldNumber
from edgepi.calibration.eeprom_mapping_pb2 import EepromLayout
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
    client_id (str)
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
        self.client_id = data_to_unpack.client_id

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

    def pack_dac_calib(self, pb: EepromLayout):
        """
        Pack dac calib dictionary to pb messages
        Args:
            pb (EepromLayout): pb dac message
        """
        for ch, calib_param in self.dac_calib_params.items():
            pb.calibs[ch].gain = calib_param.gain
            pb.calibs[ch].offset = calib_param.offset

    def pack_adc_calib(self, pb: EepromLayout):
        """
        Pack adc calib dictionary to pb messages
        Args:
            pb (EepromLayout): pb adc message
        """
        for ch, calib_param in self.adc_calib_params.items():
            pb.calibs[ch].gain = calib_param.gain
            pb.calibs[ch].offset = calib_param.offset

    def pack_rtd_calib(self, pb: EepromLayout):
        """
        Pack rtd calib dictionary to pb messages
        Args:
            pb (EepromLayout): pb rtd message
        """
        for ch, calib_param in self.rtd_calib_params.items():
            pb.calibs[ch].gain = calib_param.gain
            pb.calibs[ch].offset = calib_param.offset

    def pack_rtd_hw(self, pb: EepromLayout):
        """
        Pack rtd hardware dictionary to pb messages
        Args:
            pb (EepromLayout): pb rtd message
        """
        for indx, hw_param in self.rtd_hw_params.items():
            pb.hw_val[indx].ref_resistor = hw_param

    def pack_tc_calib(self, pb: EepromLayout):
        """
        Pack tc calib dictionary to pb messages
        Args:
            pb (EepromLayout): pb tc message
        """
        for ch, calib_param in self.tc_calib_params.items():
            pb.calibs[ch].gain = calib_param.gain
            pb.calibs[ch].offset = calib_param.offset

    def pack_tc_hw(self, pb: EepromLayout):
        """
        Pack tc hardware dictionary to pb messages
        Args:
            pb (EepromLayout): pb tc message
        """
        for indx, hw_param in self.tc_hw_params.items():
            pb.hw_val[indx].ref_resistor = hw_param

    def pack_config_key(self, pb: EepromLayout):
        """
        Pack config key dataclass to pb
        Args:
            pb (EepromLayout): pb config_key message
        """
        pb.certificate = self.config_key.certificate
        pb.private_key = self.config_key.private

    def pack_data_key(self, pb: EepromLayout):
        """
        Pack data key dataclass to pb
        Args:
            pb (EepromLayout): pb data key message
        """
        pb.certificate = self.data_key.certificate
        pb.private_key = self.data_key.private

    def pack_product_info(self, pb: EepromLayout):
        """
        Pack product data
        Args:
            pb (EepromLayout): pb data
        """
        pb.serial_number = self.serial
        pb.model = self.model
        pb.client_id = self.client_id

    def pack_dataclass(self, pb: EepromLayout, message_feild: MessageFieldNumber):
        """
        Function to populate current dictionary value to proto buffer message
        Args:
            pb (EepromLayout): protobuffer layout
            message_feild (Enum): message filed number to populate
        # """
        if message_feild == MessageFieldNumber.DAC:
            self.pack_dac_calib(pb.dac)
        elif message_feild == MessageFieldNumber.ADC:
            self.pack_adc_calib(pb.adc)
        elif message_feild == MessageFieldNumber.RTD:
            self.pack_rtd_calib(pb.rtd)
            self.pack_rtd_hw(pb.rtd)
        elif message_feild == MessageFieldNumber.TC:
            self.pack_tc_calib(pb.tc)
            self.pack_tc_hw(pb.tc)
        elif message_feild == MessageFieldNumber.CONFIGS_KEY:
            self.pack_config_key(pb.config_key)
        elif message_feild == MessageFieldNumber.DATA_KEY:
            self.pack_data_key(pb.data_key)
        elif message_feild == MessageFieldNumber.MODEL or\
             message_feild == MessageFieldNumber.CLIENT_ID or \
             message_feild == MessageFieldNumber.SERIAL:
            self.pack_product_info(pb)
        else:
            self.pack_dac_calib(pb.dac)
            self.pack_adc_calib(pb.adc)
            self.pack_rtd_calib(pb.rtd)
            self.pack_rtd_hw(pb.rtd)
            self.pack_tc_calib(pb.tc)
            self.pack_tc_hw(pb.tc)
            self.pack_config_key(pb.config_key)
            self.pack_data_key(pb.data_key)
            self.pack_product_info(pb)



            