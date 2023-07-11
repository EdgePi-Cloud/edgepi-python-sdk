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
    def extract_rtd_calib_params(key_pb: keys_pb2):
        """De-serialize method"""
        key_mod = AwsKeys()
        if key_pb.HasField("private_key"):
            key_mod.private_key = key_pb.private_key
        if key_pb.HasField("certificate"):
            key_mod.certificate = key_pb.certificate
        return key_mod
