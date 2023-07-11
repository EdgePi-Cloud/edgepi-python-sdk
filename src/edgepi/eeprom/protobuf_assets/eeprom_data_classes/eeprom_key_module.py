"""EEPROM key module Dataclass"""
from dataclasses import dataclass
from edgepi.eeprom.protobuf_assets.generated_pb2 import keys_pb2



@dataclass
class AwsKeys:
    """Key Pair dataclass"""
    private_key:str = None
    certificate:str = None

    def populate_rtd_module_pb(self, key_pb: keys_pb2):
        """serialize method"""
        if self.rtd is not None:
            key_pb.private_key = self.private_key
            key_pb.certificate = self.certificate

    @staticmethod
    def extract_rtd_calib_params(rtd_pb: keys_pb2):
        """De-serialize method"""
        rtd_mod = AwsKeys()
        if rtd_pb.HasField("private_key"):
            rtd_mod.rtd = CalibParam(gain=rtd_pb.rtd.gain, offset = rtd_pb.rtd.offset)
        if rtd_pb.HasField("rtd_resistor"):
            rtd_mod.rtd_resistor = rtd_pb.rtd_resistor
        return rtd_mod
