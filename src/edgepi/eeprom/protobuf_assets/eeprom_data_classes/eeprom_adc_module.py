"""EEPROM ADC Module Dataclass"""
from dataclasses import dataclass
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.eeprom.protobuf_assets.generated_pb2 import adc_module_pb2

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

    def extract_ch_dict(self):
        """create channel to calibration param dictionary"""
        ch_dict = {
            0:self.adc_ch_1,
            1:self.adc_ch_2,
            2:self.adc_ch_3,
            3:self.adc_ch_4,
            4:self.adc_ch_5,
            5:self.adc_ch_6,
            6:self.adc_ch_7,
            7:self.adc_ch_8,
            8:self.adc_diff_1,
            9:self.adc_diff_2,
            10:self.adc_diff_3,
            11:self.adc_diff_4,
        }
        return ch_dict
