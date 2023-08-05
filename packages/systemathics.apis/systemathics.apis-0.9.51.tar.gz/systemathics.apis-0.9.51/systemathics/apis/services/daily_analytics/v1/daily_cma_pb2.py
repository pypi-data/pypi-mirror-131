# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/services/daily_analytics/v1/daily_cma.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.type import date_pb2 as google_dot_type_dot_date__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from systemathics.apis.type.shared.v1 import identifier_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2
from systemathics.apis.type.shared.v1 import constraints_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2
from systemathics.apis.type.shared.v1 import status_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='systemathics/apis/services/daily_analytics/v1/daily_cma.proto',
  package='systemathics.apis.services.daily_analytics.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n=systemathics/apis/services/daily_analytics/v1/daily_cma.proto\x12-systemathics.apis.services.daily_analytics.v1\x1a\x16google/type/date.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x31systemathics/apis/type/shared/v1/identifier.proto\x1a\x32systemathics/apis/type/shared/v1/constraints.proto\x1a-systemathics/apis/type/shared/v1/status.proto\"\xab\x01\n\x0f\x44\x61ilyCmaRequest\x12@\n\nidentifier\x18\x01 \x01(\x0b\x32,.systemathics.apis.type.shared.v1.Identifier\x12\x42\n\x0b\x63onstraints\x18\x02 \x01(\x0b\x32-.systemathics.apis.type.shared.v1.Constraints\x12\x12\n\nadjustment\x18\x03 \x01(\x08\"\x97\x01\n\x10\x44\x61ilyCmaResponse\x12I\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32;.systemathics.apis.services.daily_analytics.v1.DailyCmaData\x12\x38\n\x06status\x18\x02 \x01(\x0b\x32(.systemathics.apis.type.shared.v1.Status\"O\n\x0c\x44\x61ilyCmaData\x12\x1f\n\x04\x64\x61te\x18\x01 \x01(\x0b\x32\x11.google.type.Date\x12\r\n\x05value\x18\x02 \x01(\x01\x12\x0f\n\x07\x61verage\x18\x03 \x01(\x01\x32\x9f\x01\n\x0f\x44\x61ilyCmaService\x12\x8b\x01\n\x08\x44\x61ilyCma\x12>.systemathics.apis.services.daily_analytics.v1.DailyCmaRequest\x1a?.systemathics.apis.services.daily_analytics.v1.DailyCmaResponseb\x06proto3'
  ,
  dependencies=[google_dot_type_dot_date__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_status__pb2.DESCRIPTOR,])




_DAILYCMAREQUEST = _descriptor.Descriptor(
  name='DailyCmaRequest',
  full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaRequest.identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='constraints', full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaRequest.constraints', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='adjustment', full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaRequest.adjustment', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=319,
  serialized_end=490,
)


_DAILYCMARESPONSE = _descriptor.Descriptor(
  name='DailyCmaResponse',
  full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaResponse.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaResponse.status', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=493,
  serialized_end=644,
)


_DAILYCMADATA = _descriptor.Descriptor(
  name='DailyCmaData',
  full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='date', full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaData.date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaData.value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='average', full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaData.average', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=646,
  serialized_end=725,
)

_DAILYCMAREQUEST.fields_by_name['identifier'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2._IDENTIFIER
_DAILYCMAREQUEST.fields_by_name['constraints'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2._CONSTRAINTS
_DAILYCMARESPONSE.fields_by_name['data'].message_type = _DAILYCMADATA
_DAILYCMARESPONSE.fields_by_name['status'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_status__pb2._STATUS
_DAILYCMADATA.fields_by_name['date'].message_type = google_dot_type_dot_date__pb2._DATE
DESCRIPTOR.message_types_by_name['DailyCmaRequest'] = _DAILYCMAREQUEST
DESCRIPTOR.message_types_by_name['DailyCmaResponse'] = _DAILYCMARESPONSE
DESCRIPTOR.message_types_by_name['DailyCmaData'] = _DAILYCMADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DailyCmaRequest = _reflection.GeneratedProtocolMessageType('DailyCmaRequest', (_message.Message,), {
  'DESCRIPTOR' : _DAILYCMAREQUEST,
  '__module__' : 'systemathics.apis.services.daily_analytics.v1.daily_cma_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.daily_analytics.v1.DailyCmaRequest)
  })
_sym_db.RegisterMessage(DailyCmaRequest)

DailyCmaResponse = _reflection.GeneratedProtocolMessageType('DailyCmaResponse', (_message.Message,), {
  'DESCRIPTOR' : _DAILYCMARESPONSE,
  '__module__' : 'systemathics.apis.services.daily_analytics.v1.daily_cma_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.daily_analytics.v1.DailyCmaResponse)
  })
_sym_db.RegisterMessage(DailyCmaResponse)

DailyCmaData = _reflection.GeneratedProtocolMessageType('DailyCmaData', (_message.Message,), {
  'DESCRIPTOR' : _DAILYCMADATA,
  '__module__' : 'systemathics.apis.services.daily_analytics.v1.daily_cma_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.daily_analytics.v1.DailyCmaData)
  })
_sym_db.RegisterMessage(DailyCmaData)



_DAILYCMASERVICE = _descriptor.ServiceDescriptor(
  name='DailyCmaService',
  full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=728,
  serialized_end=887,
  methods=[
  _descriptor.MethodDescriptor(
    name='DailyCma',
    full_name='systemathics.apis.services.daily_analytics.v1.DailyCmaService.DailyCma',
    index=0,
    containing_service=None,
    input_type=_DAILYCMAREQUEST,
    output_type=_DAILYCMARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DAILYCMASERVICE)

DESCRIPTOR.services_by_name['DailyCmaService'] = _DAILYCMASERVICE

# @@protoc_insertion_point(module_scope)
