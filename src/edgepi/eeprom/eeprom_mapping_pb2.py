# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: edgepi/calibration/eeprom_mapping.proto
"""Generated protocol buffer code."""
# pylint: skip-file
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'edgepi/calibration/eeprom_mapping.proto\"\xd1\x05\n\x0c\x45\x65promLayout\x12,\n\x03\x64\x61\x63\x18\x01 \x01(\x0b\x32\x1f.EepromLayout.ModuleCalibParams\x12,\n\x03\x61\x64\x63\x18\x02 \x01(\x0b\x32\x1f.EepromLayout.ModuleCalibParams\x12,\n\x03rtd\x18\x03 \x01(\x0b\x32\x1f.EepromLayout.ModuleCalibParams\x12+\n\x02tc\x18\x04 \x01(\x0b\x32\x1f.EepromLayout.ModuleCalibParams\x12(\n\nconfig_key\x18\x05 \x01(\x0b\x32\x14.EepromLayout.AwsKey\x12&\n\x08\x64\x61ta_key\x18\x06 \x01(\x0b\x32\x14.EepromLayout.AwsKey\x12\x15\n\rserial_number\x18\x07 \x01(\t\x12\r\n\x05model\x18\x08 \x01(\t\x12\x18\n\x10\x63lient_id_config\x18\t \x01(\t\x12\x16\n\x0e\x63lient_id_data\x18\n \x01(\t\x12\x10\n\x08thing_id\x18\x0b \x01(\t\x1a\x99\x02\n\x11ModuleCalibParams\x12<\n\x06\x63\x61libs\x18\x01 \x03(\x0b\x32,.EepromLayout.ModuleCalibParams.ChannelCalib\x12=\n\x06hw_val\x18\x02 \x03(\x0b\x32-.EepromLayout.ModuleCalibParams.HardwareValue\x1aJ\n\x0c\x43hannelCalib\x12\x11\n\x04gain\x18\x01 \x01(\x02H\x00\x88\x01\x01\x12\x13\n\x06offset\x18\x02 \x01(\x02H\x01\x88\x01\x01\x42\x07\n\x05_gainB\t\n\x07_offset\x1a;\n\rHardwareValue\x12\x19\n\x0cref_resistor\x18\x01 \x01(\x02H\x00\x88\x01\x01\x42\x0f\n\r_ref_resistor\x1a\x32\n\x06\x41wsKey\x12\x13\n\x0bprivate_key\x18\x01 \x01(\t\x12\x13\n\x0b\x63\x65rtificate\x18\x02 \x01(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'edgepi.calibration.eeprom_mapping_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_EEPROMLAYOUT']._serialized_start=44
  _globals['_EEPROMLAYOUT']._serialized_end=765
  _globals['_EEPROMLAYOUT_MODULECALIBPARAMS']._serialized_start=432
  _globals['_EEPROMLAYOUT_MODULECALIBPARAMS']._serialized_end=713
  _globals['_EEPROMLAYOUT_MODULECALIBPARAMS_CHANNELCALIB']._serialized_start=578
  _globals['_EEPROMLAYOUT_MODULECALIBPARAMS_CHANNELCALIB']._serialized_end=652
  _globals['_EEPROMLAYOUT_MODULECALIBPARAMS_HARDWAREVALUE']._serialized_start=654
  _globals['_EEPROMLAYOUT_MODULECALIBPARAMS_HARDWAREVALUE']._serialized_end=713
  _globals['_EEPROMLAYOUT_AWSKEY']._serialized_start=715
  _globals['_EEPROMLAYOUT_AWSKEY']._serialized_end=765
# @@protoc_insertion_point(module_scope)