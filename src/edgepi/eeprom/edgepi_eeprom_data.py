"""EdgePi EEPROM Dataclass"""
from dataclasses import dataclass

from edgepi.eeprom.protobuf_assets.generated_pb2 import (
    edgepi_module_pb2,
    dac_module_pb2,
    adc_module_pb2,
    rtd_module_pb2,
    tc_module_pb2,
    keys_pb2
)
from edgepi.eeprom.protobuf_assets.eeprom_data_classes.eeprom_dac_module import DACModule
from edgepi.eeprom.protobuf_assets.eeprom_data_classes.eeprom_adc_module import ADCModule
from edgepi.eeprom.protobuf_assets.eeprom_data_classes.eeprom_rtd_module import RTDModule
from edgepi.eeprom.protobuf_assets.eeprom_data_classes.eeprom_tc_module import TCModule
from edgepi.eeprom.protobuf_assets.eeprom_data_classes.eeprom_key_module import AwsKeys

@dataclass
class EepromDataClass:
    """EEPROM Dataclass"""
    # pylint: disable=too-many-instance-attributes
    dac_calib_params: DACModule = None
    adc1_calib_params: ADCModule = None
    adc2_calib_params: ADCModule = None
    rtd_calib_params: RTDModule = None
    tc_calib_params: TCModule = None
    config_key: AwsKeys = AwsKeys(None, None)
    data_key: AwsKeys = AwsKeys(None, None)
    serial:str = None
    model:str = None
    cm_part_number: str = None
    tb_part_number: str = None
    cm4_part_number: str = None

    def populate_eeprom_module(self, eeprom_pb:edgepi_module_pb2):
        """Serialize"""
        self.__populate_dac_module(eeprom_pb.dac_module)
        self.__populate_adc1_module(eeprom_pb.adc1_module)
        self.__populate_adc2_module(eeprom_pb.adc2_module)
        self.__populate_rtd_module(eeprom_pb.rtd_module)
        self.__populate_tc_module(eeprom_pb.tc_module)
        self.__populate_config_key_module(eeprom_pb.config_keys)
        self.__populate_data_key_module(eeprom_pb.data_keys)

        if self.serial is not None:
            eeprom_pb.serial_number = self.serial
        if self.model is not None:
            eeprom_pb.model = self.model
        if self.cm_part_number is not None:
            eeprom_pb.cm_part_number = self.cm_part_number
        if self.tb_part_number is not None:
            eeprom_pb.tb_part_number = self.tb_part_number
        if self.cm4_part_number is not None:
            eeprom_pb.cm4_part_number = self.cm4_part_number

    def __populate_dac_module(self, dac_pb: dac_module_pb2):
        """Serialize DAC"""
        if self.dac_calib_params is None:
            return
        self.dac_calib_params.populate_dac_module_pb(dac_pb)

    def __populate_adc1_module(self, adc_pb: adc_module_pb2):
        """Serialize ADC1"""
        if self.adc1_calib_params is None:
            return
        self.adc1_calib_params.populate_adc_module_pb(adc_pb)

    def __populate_adc2_module(self, adc_pb: adc_module_pb2):
        """Serialize ADC2"""
        if self.adc2_calib_params is None:
            return
        self.adc2_calib_params.populate_adc_module_pb(adc_pb)

    def __populate_rtd_module(self, rtd_pb: rtd_module_pb2):
        """Serialize RTD"""
        if self.rtd_calib_params is None:
            return
        self.rtd_calib_params.populate_rtd_module_pb(rtd_pb)
    def __populate_tc_module(self, tc_pb: tc_module_pb2):
        """Serialize TC"""
        if self.tc_calib_params is None:
            return
        self.tc_calib_params.populate_tc_module_pb(tc_pb)

    def __populate_config_key_module(self, key_pb: keys_pb2):
        """Serialize Config Keys"""
        if self.config_key is None:
            return
        self.config_key.populate_keys_pb(key_pb)

    def __populate_data_key_module(self, key_pb: keys_pb2):
        """Serialize Data Keys"""
        if self.data_key is None:
            return
        self.data_key.populate_keys_pb(key_pb)

    @staticmethod
    def extract_eeprom_data(eeprom_pb:edgepi_module_pb2):
        """De-serialize"""
        eeprom_data = EepromDataClass()
        eeprom_data.dac_calib_params = EepromDataClass.extract_dac_data(eeprom_pb.dac_module)
        eeprom_data.adc1_calib_params = EepromDataClass.extract_adc_data(eeprom_pb.adc1_module)
        eeprom_data.adc2_calib_params = EepromDataClass.extract_adc_data(eeprom_pb.adc2_module)
        eeprom_data.rtd_calib_params = EepromDataClass.extract_rtd_data(eeprom_pb.rtd_module)
        eeprom_data.tc_calib_params = EepromDataClass.extract_tc_data(eeprom_pb.tc_module)

        if eeprom_pb.HasField("config_keys"):
            eeprom_data.config_key = EepromDataClass.extract_config_key(eeprom_pb.config_keys)
        if eeprom_pb.HasField("data_keys"):
            eeprom_data.data_key = EepromDataClass.extract_data_key(eeprom_pb.data_keys)
        if eeprom_pb.HasField("serial_number"):
            eeprom_data.serial = eeprom_pb.serial_number
        if eeprom_pb.HasField("model"):
            eeprom_data.model = eeprom_pb.model
        if eeprom_pb.HasField("cm_part_number"):
            eeprom_data.cm_part_number = eeprom_pb.cm_part_number
        if eeprom_pb.HasField("tb_part_number"):
            eeprom_data.tb_part_number = eeprom_pb.tb_part_number
        if eeprom_pb.HasField("cm4_part_number"):
            eeprom_data.cm4_part_number = eeprom_pb.cm4_part_number

        return eeprom_data

    # pylint: disable=inconsistent-return-statements
    @staticmethod
    def extract_dac_data(dac_pb: dac_module_pb2):
        """De-serialize DAC"""
        if dac_pb is None:
            return
        return DACModule.extract_dac_calib_params(dac_pb)

    @staticmethod
    def extract_adc_data(adc_pb: adc_module_pb2):
        """De-serialize ADC"""
        if adc_pb is None:
            return
        return ADCModule.extract_adc_calib_params(adc_pb)

    @staticmethod
    def extract_rtd_data(rtd_pb: rtd_module_pb2):
        """De-serialize RTD"""
        if rtd_pb is None:
            return
        return RTDModule.extract_rtd_calib_params(rtd_pb)

    @staticmethod
    def extract_tc_data(tc_pb: tc_module_pb2):
        """De-serialize TC"""
        if tc_pb is None:
            return
        return TCModule.extract_tc_calib_params(tc_pb)

    @staticmethod
    def extract_config_key(key_pb: keys_pb2):
        """De-serialize Config Keys"""
        return AwsKeys.extract_keys(key_pb)

    @staticmethod
    def extract_data_key(key_pb: keys_pb2):
        """De-serialize Data Keys"""
        return AwsKeys.extract_keys(key_pb)
