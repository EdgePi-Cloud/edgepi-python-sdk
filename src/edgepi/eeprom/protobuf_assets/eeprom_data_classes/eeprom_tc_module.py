"""EEPROM RTD module Dataclass"""
from dataclasses import dataclass
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.eeprom.protobuf_assets.generated_pb2 import tc_module_pb2

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
