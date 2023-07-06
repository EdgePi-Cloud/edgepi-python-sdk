"""EEPROM DAC module Dataclass"""
from dataclasses import dataclass
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.eeprom.protobuf_assets.generated_pb2 import dac_module_pb2

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

    def extract_ch_dict(self):
        """create channel to calibration param dictionary"""
        ch_dict = {
            0:self.dac_ch_1,
            1:self.dac_ch_2,
            2:self.dac_ch_3,
            3:self.dac_ch_4,
            4:self.dac_ch_5,
            5:self.dac_ch_6,
            6:self.dac_ch_7,
            7:self.dac_ch_8,
        }
        return ch_dict
