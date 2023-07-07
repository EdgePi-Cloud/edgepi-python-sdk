"""EEPROM RTD module Dataclass"""
from dataclasses import dataclass
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.eeprom.protobuf_assets.generated_pb2 import rtd_module_pb2

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
