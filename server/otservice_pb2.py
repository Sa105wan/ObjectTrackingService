# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: otservice.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'otservice.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fotservice.proto\x12\totservice\"1\n\x0cVideoRequest\x12\x12\n\nvideo_file\x18\x01 \x01(\x0c\x12\r\n\x05model\x18\x02 \x01(\t\"1\n\rVideoResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"^\n\x08LogEntry\x12\x12\n\nip_address\x18\x01 \x01(\t\x12!\n\x19grpc_system_response_time\x18\x02 \x01(\x01\x12\x1b\n\x13total_response_time\x18\x03 \x01(\x01\"/\n\x0bLogResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\x90\x01\n\tOtService\x12\x44\n\x0bUploadVideo\x12\x17.otservice.VideoRequest\x1a\x18.otservice.VideoResponse\"\x00(\x01\x12=\n\x0cSendLogEntry\x12\x13.otservice.LogEntry\x1a\x16.otservice.LogResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'otservice_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VIDEOREQUEST']._serialized_start=30
  _globals['_VIDEOREQUEST']._serialized_end=79
  _globals['_VIDEORESPONSE']._serialized_start=81
  _globals['_VIDEORESPONSE']._serialized_end=130
  _globals['_LOGENTRY']._serialized_start=132
  _globals['_LOGENTRY']._serialized_end=226
  _globals['_LOGRESPONSE']._serialized_start=228
  _globals['_LOGRESPONSE']._serialized_end=275
  _globals['_OTSERVICE']._serialized_start=278
  _globals['_OTSERVICE']._serialized_end=422
# @@protoc_insertion_point(module_scope)
