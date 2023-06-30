"""EdgePi EEPROM Dataclass"""
from dataclasses import dataclass

from edgepi.calibration.calibration_constants import CalibParam
from edgepi.eeprom.proto_files import (
    edgepi_module_pb2,
    dac_module_pb2,
    adc_module_pb2,
    rtd_module_pb2,
    tc_module_pb2
)

@dataclass
class AwsKeys:
    """Key Pair dataclass"""
    private_key:str = None
    certificate:str = None

@dataclass
class DACModule:
# pylint: disable=too-many-instance-attributes
    """DAC module dataclass"""
    dac_ch_1: CalibParam = None
    dac_ch_2: CalibParam = None
    dac_ch_3: CalibParam = None
    dac_ch_4: CalibParam = None
    dac_ch_5: CalibParam = None
    dac_ch_6: CalibParam = None
    dac_ch_7: CalibParam = None
    dac_ch_8: CalibParam = None

    def populate_dac_module_pb(self, dac_pb: dac_module_pb2):
        """serialize method"""
        # DAC
        if self.dac_ch_1 is not None:
            dac_pb.dac_ch_1.gain = self.dac_ch_1.gain
            dac_pb.dac_ch_1.offset = self.dac_ch_1.offset
        if self.dac_ch_2 is not None:
            dac_pb.dac_ch_2.gain = self.dac_ch_2.gain
            dac_pb.dac_ch_2.offset = self.dac_ch_2.offset
        if self.dac_ch_3 is not None:
            dac_pb.dac_ch_3.gain = self.dac_ch_3.gain
            dac_pb.dac_ch_3.offset = self.dac_ch_3.offset
        if self.dac_ch_4 is not None:
            dac_pb.dac_ch_4.gain = self.dac_ch_4.gain
            dac_pb.dac_ch_4.offset = self.dac_ch_4.offset
        if self.dac_ch_5 is not None:
            dac_pb.dac_ch_5.gain = self.dac_ch_5.gain
            dac_pb.dac_ch_5.offset = self.dac_ch_5.offset
        if self.dac_ch_6 is not None:
            dac_pb.dac_ch_6.gain = self.dac_ch_6.gain
            dac_pb.dac_ch_6.offset = self.dac_ch_6.offset
        if self.dac_ch_7 is not None:
            dac_pb.dac_ch_7.gain = self.dac_ch_7.gain
            dac_pb.dac_ch_7.offset = self.dac_ch_7.offset
        if self.dac_ch_8 is not None:
            dac_pb.dac_ch_8.gain = self.dac_ch_8.gain
            dac_pb.dac_ch_8.offset = self.dac_ch_8.offset

    @staticmethod
    def extract_dac_calib_params(dac_pb: dac_module_pb2):
        """De-serialize method"""
        dac_mod = DACModule()
        # DAC
        if dac_pb.HasField("dac_ch_1"):
            dac_mod.dac_ch_1 = CalibParam(gain=dac_pb.dac_ch_1.gain, offset=dac_pb.dac_ch_1.offset)
        if dac_pb.HasField("dac_ch_2"):
            dac_mod.dac_ch_2 = CalibParam(gain=dac_pb.dac_ch_2.gain, offset=dac_pb.dac_ch_2.offset)
        if dac_pb.HasField("dac_ch_3"):
            dac_mod.dac_ch_3 = CalibParam(gain=dac_pb.dac_ch_3.gain, offset=dac_pb.dac_ch_3.offset)
        if dac_pb.HasField("dac_ch_4"):
            dac_mod.dac_ch_4 = CalibParam(gain=dac_pb.dac_ch_4.gain, offset=dac_pb.dac_ch_4.offset)
        if dac_pb.HasField("dac_ch_5"):
            dac_mod.dac_ch_5 = CalibParam(gain=dac_pb.dac_ch_5.gain, offset=dac_pb.dac_ch_5.offset)
        if dac_pb.HasField("dac_ch_6"):
            dac_mod.dac_ch_6 = CalibParam(gain=dac_pb.dac_ch_6.gain, offset=dac_pb.dac_ch_6.offset)
        if dac_pb.HasField("dac_ch_7"):
            dac_mod.dac_ch_7 = CalibParam(gain=dac_pb.dac_ch_7.gain, offset=dac_pb.dac_ch_7.offset)
        if dac_pb.HasField("dac_ch_8"):
            dac_mod.dac_ch_8 = CalibParam(gain=dac_pb.dac_ch_8.gain, offset=dac_pb.dac_ch_8.offset)
        return dac_mod


@dataclass
class ADCModule:
    """ADC Module Dataclass"""
    # pylint: disable=too-many-instance-attributes
    adc_ch_1: CalibParam = None
    adc_ch_2: CalibParam = None
    adc_ch_3: CalibParam = None
    adc_ch_4: CalibParam = None
    adc_ch_5: CalibParam = None
    adc_ch_6: CalibParam = None
    adc_ch_7: CalibParam = None
    adc_ch_8: CalibParam = None

    adc_diff_1: CalibParam = None
    adc_diff_2: CalibParam = None
    adc_diff_3: CalibParam = None
    adc_diff_4: CalibParam = None

    def populate_adc_module_pb(self, adc_pb: adc_module_pb2):
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        """serialize method"""
        # adc Single ended
        if self.adc_ch_1 is not None:
            adc_pb.adc_ch_1.gain = self.adc_ch_1.gain
            adc_pb.adc_ch_1.offset = self.adc_ch_1.offset
        if self.adc_ch_2 is not None:
            adc_pb.adc_ch_2.gain = self.adc_ch_2.gain
            adc_pb.adc_ch_2.offset = self.adc_ch_2.offset
        if self.adc_ch_3 is not None:
            adc_pb.adc_ch_3.gain = self.adc_ch_3.gain
            adc_pb.adc_ch_3.offset = self.adc_ch_3.offset
        if self.adc_ch_4 is not None:
            adc_pb.adc_ch_4.gain = self.adc_ch_4.gain
            adc_pb.adc_ch_4.offset = self.adc_ch_4.offset
        if self.adc_ch_5 is not None:
            adc_pb.adc_ch_5.gain = self.adc_ch_5.gain
            adc_pb.adc_ch_5.offset = self.adc_ch_5.offset
        if self.adc_ch_6 is not None:
            adc_pb.adc_ch_6.gain = self.adc_ch_6.gain
            adc_pb.adc_ch_6.offset = self.adc_ch_6.offset
        if self.adc_ch_7 is not None:
            adc_pb.adc_ch_7.gain = self.adc_ch_7.gain
            adc_pb.adc_ch_7.offset = self.adc_ch_7.offset
        if self.adc_ch_8 is not None:
            adc_pb.adc_ch_8.gain = self.adc_ch_8.gain
            adc_pb.adc_ch_8.offset = self.adc_ch_8.offset
        # adc Differential
        if self.adc_diff_1 is not None:
            adc_pb.adc_diff_1.gain = self.adc_diff_1.gain
            adc_pb.adc_diff_1.offset = self.adc_diff_1.offset
        if self.adc_diff_2 is not None:
            adc_pb.adc_diff_2.gain = self.adc_diff_2.gain
            adc_pb.adc_diff_2.offset = self.adc_diff_2.offset
        if self.adc_diff_3 is not None:
            adc_pb.adc_diff_3.gain = self.adc_diff_3.gain
            adc_pb.adc_diff_3.offset = self.adc_diff_3.offset
        if self.adc_diff_4 is not None:
            adc_pb.adc_diff_4.gain = self.adc_diff_4.gain
            adc_pb.adc_diff_4.offset = self.adc_diff_4.offset

    @staticmethod
    def extract_adc_calib_params(adc_pb: adc_module_pb2):
        # pylint: disable=too-many-branches
        """De-serialize method"""
        adc_mod = ADCModule()
        # adc Single Ended
        if adc_pb.HasField("adc_ch_1"):
            adc_mod.adc_ch_1=CalibParam(gain=adc_pb.adc_ch_1.gain, offset=adc_pb.adc_ch_1.offset)
        if adc_pb.HasField("adc_ch_2"):
            adc_mod.adc_ch_2=CalibParam(gain=adc_pb.adc_ch_2.gain, offset=adc_pb.adc_ch_2.offset)
        if adc_pb.HasField("adc_ch_3"):
            adc_mod.adc_ch_3=CalibParam(gain=adc_pb.adc_ch_3.gain, offset=adc_pb.adc_ch_3.offset)
        if adc_pb.HasField("adc_ch_4"):
            adc_mod.adc_ch_4=CalibParam(gain=adc_pb.adc_ch_4.gain, offset=adc_pb.adc_ch_4.offset)
        if adc_pb.HasField("adc_ch_5"):
            adc_mod.adc_ch_5=CalibParam(gain=adc_pb.adc_ch_5.gain, offset=adc_pb.adc_ch_5.offset)
        if adc_pb.HasField("adc_ch_6"):
            adc_mod.adc_ch_6=CalibParam(gain=adc_pb.adc_ch_6.gain, offset=adc_pb.adc_ch_6.offset)
        if adc_pb.HasField("adc_ch_7"):
            adc_mod.adc_ch_7=CalibParam(gain=adc_pb.adc_ch_7.gain, offset=adc_pb.adc_ch_7.offset)
        if adc_pb.HasField("adc_ch_8"):
            adc_mod.adc_ch_8=CalibParam(gain=adc_pb.adc_ch_8.gain, offset=adc_pb.adc_ch_8.offset)
        # adc Differential
        if adc_pb.HasField("adc_diff_1"):
            adc_mod.adc_diff_1 = CalibParam(gain=adc_pb.adc_diff_1.gain,
                                             offset=adc_pb.adc_diff_1.offset)
        if adc_pb.HasField("adc_diff_2"):
            adc_mod.adc_diff_2 = CalibParam(gain=adc_pb.adc_diff_2.gain,
                                             offset=adc_pb.adc_diff_2.offset)
        if adc_pb.HasField("adc_diff_3"):
            adc_mod.adc_diff_3 = CalibParam(gain=adc_pb.adc_diff_3.gain,
                                             offset=adc_pb.adc_diff_3.offset)
        if adc_pb.HasField("adc_diff_4"):
            adc_mod.adc_diff_4 = CalibParam(gain=adc_pb.adc_diff_4.gain,
                                             offset=adc_pb.adc_diff_4.offset)
        return adc_mod

@dataclass
class RTDModule:
    """RTD Module Dataclass"""
    rtd: CalibParam = None
    rtd_resistor: float = None

    def populate_rtd_module_pb(self, rtd_pb: rtd_module_pb2):
        """serialize method"""
        if self.rtd is not None:
            rtd_pb.rtd.gain = self.rtd.gain
            rtd_pb.rtd.offset = self.rtd.offset
        if self.rtd_resistor is not None:
            rtd_pb.rtd_resistor = self.rtd_resistor

    @staticmethod
    def extract_rtd_calib_params(rtd_pb: rtd_module_pb2):
        """De-serialize method"""
        rtd_mod = RTDModule()
        if rtd_pb.HasField("rtd"):
            rtd_mod.rtd = CalibParam(gain=rtd_pb.rtd.gain, offset = rtd_pb.rtd.offset)
        if rtd_pb.HasField("rtd_resistor"):
            rtd_mod.rtd_resistor = rtd_pb.rtd_resistor
        return rtd_mod

@dataclass
class TCModule:
    """TC module dataclass"""
    # pylint: disable=invalid-name
    # pylint: disable=too-many-instance-attributes
    tc_B: CalibParam = None
    tc_E: CalibParam = None
    tc_J: CalibParam = None
    tc_K: CalibParam = None
    tc_N: CalibParam = None
    tc_R: CalibParam = None
    tc_S: CalibParam = None
    tc_T: CalibParam = None

    def populate_tc_module_pb(self, tc_pb: tc_module_pb2):
        """serialize method"""
        if self.tc_B is not None:
            tc_pb.tc_B.gain = self.tc_B.gain
            tc_pb.tc_B.offset = self.tc_B.offset
        if self.tc_E is not None:
            tc_pb.tc_E.gain = self.tc_E.gain
            tc_pb.tc_E.offset = self.tc_E.offset
        if self.tc_J is not None:
            tc_pb.tc_J.gain = self.tc_J.gain
            tc_pb.tc_J.offset = self.tc_J.offset
        if self.tc_K is not None:
            tc_pb.tc_K.gain = self.tc_K.gain
            tc_pb.tc_K.offset = self.tc_K.offset
        if self.tc_N is not None:
            tc_pb.tc_N.gain = self.tc_N.gain
            tc_pb.tc_N.offset = self.tc_N.offset
        if self.tc_R is not None:
            tc_pb.tc_R.gain = self.tc_R.gain
            tc_pb.tc_R.offset = self.tc_R.offset
        if self.tc_S is not None:
            tc_pb.tc_S.gain = self.tc_S.gain
            tc_pb.tc_S.offset = self.tc_S.offset
        if self.tc_T is not None:
            tc_pb.tc_T.gain = self.tc_T.gain
            tc_pb.tc_T.offset = self.tc_T.offset

    @staticmethod
    def extract_tc_calib_params(tc_pb: tc_module_pb2):
        """De-serialize method"""
        tc_mod = TCModule()
        if tc_pb.HasField("tc_B"):
            tc_mod.tc_B = CalibParam(gain=tc_pb.tc_B.gain, offset = tc_pb.tc_B.offset)
        if tc_pb.HasField("tc_E"):
            tc_mod.tc_E = CalibParam(gain=tc_pb.tc_E.gain, offset = tc_pb.tc_E.offset)
        if tc_pb.HasField("tc_J"):
            tc_mod.tc_J = CalibParam(gain=tc_pb.tc_J.gain, offset = tc_pb.tc_J.offset)
        if tc_pb.HasField("tc_K"):
            tc_mod.tc_K = CalibParam(gain=tc_pb.tc_K.gain, offset = tc_pb.tc_K.offset)
        if tc_pb.HasField("tc_N"):
            tc_mod.tc_N = CalibParam(gain=tc_pb.tc_N.gain, offset = tc_pb.tc_N.offset)
        if tc_pb.HasField("tc_R"):
            tc_mod.tc_R = CalibParam(gain=tc_pb.tc_R.gain, offset = tc_pb.tc_R.offset)
        if tc_pb.HasField("tc_S"):
            tc_mod.tc_S = CalibParam(gain=tc_pb.tc_S.gain, offset = tc_pb.tc_S.offset)
        if tc_pb.HasField("tc_T"):
            tc_mod.tc_T = CalibParam(gain=tc_pb.tc_T.gain, offset = tc_pb.tc_T.offset)
        return tc_mod

@dataclass
class EepromDataClass:
    """EEPROM Dataclass"""
    # pylint: disable=too-many-instance-attributes
    dac_calib_params: DACModule = None
    adc1_calib_params: ADCModule = None
    adc2_calib_params: ADCModule = None
    rtd_calib_params: RTDModule = None
    tc_calib_params: TCModule = None
    config_key: AwsKeys = None
    data_key: AwsKeys = None
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

        if self.config_key is not None:
            eeprom_pb.config_keys.certificate = self.config_key.certificate
            eeprom_pb.config_keys.private_key = self.config_key.private_key
        if self.data_key is not None:
            eeprom_pb.data_keys.certificate = self.data_key.certificate
            eeprom_pb.data_keys.private_key = self.data_key.private_key
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

    @staticmethod
    def extract_eeprom_data(eeprom_pb:edgepi_module_pb2):
        """De-serialize"""
        eeprom_data = EepromDataClass()
        eeprom_data.dac_calib_params = EepromDataClass.extract_dac_data(eeprom_pb.dac_module)
        eeprom_data.adc1_calib_params = EepromDataClass.extract_adc_data(eeprom_pb.adc1_module)
        eeprom_data.adc2_calib_params = EepromDataClass.extract_adc_data(eeprom_pb.adc2_module)
        eeprom_data.rtd_calib_params = EepromDataClass.extract_rtd_data(eeprom_pb.rtd_module)
        eeprom_data.tc_calib_params = EepromDataClass.extract_tc_data(eeprom_pb.tc_module)

        if eeprom_pb.HasField("serial_number"):
            eeprom_data.serial = eeprom_pb.serial_number
        if eeprom_pb.HasField("model"):
            eeprom_data.model = eeprom_pb.model
        if eeprom_pb.HasField("config_keys"):
            eeprom_data.config_key = eeprom_pb.config_keys
        if eeprom_pb.HasField("data_keys"):
            eeprom_data.data_key = eeprom_pb.data_keys
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
