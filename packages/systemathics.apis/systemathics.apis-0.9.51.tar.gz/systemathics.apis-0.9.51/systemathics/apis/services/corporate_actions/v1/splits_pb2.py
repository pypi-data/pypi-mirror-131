# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/services/corporate_actions/v1/splits.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.type import date_pb2 as google_dot_type_dot_date__pb2
from systemathics.apis.type.shared.v1 import identifier_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2
from systemathics.apis.type.shared.v1 import constraints_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2
from systemathics.apis.type.shared.v1 import status_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='systemathics/apis/services/corporate_actions/v1/splits.proto',
  package='systemathics.apis.services.corporate_actions.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n<systemathics/apis/services/corporate_actions/v1/splits.proto\x12/systemathics.apis.services.corporate_actions.v1\x1a\x16google/type/date.proto\x1a\x31systemathics/apis/type/shared/v1/identifier.proto\x1a\x32systemathics/apis/type/shared/v1/constraints.proto\x1a-systemathics/apis/type/shared/v1/status.proto\"\x95\x01\n\rSplitsRequest\x12@\n\nidentifier\x18\x01 \x01(\x0b\x32,.systemathics.apis.type.shared.v1.Identifier\x12\x42\n\x0b\x63onstraints\x18\x02 \x01(\x0b\x32-.systemathics.apis.type.shared.v1.Constraints\"\x90\x01\n\x0eSplitsResponse\x12\x44\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x36.systemathics.apis.services.corporate_actions.v1.Split\x12\x38\n\x06status\x18\x02 \x01(\x0b\x32(.systemathics.apis.type.shared.v1.Status\"_\n\x05Split\x12\x1f\n\x04\x64\x61te\x18\x01 \x01(\x0b\x32\x11.google.type.Date\x12\x12\n\nnew_shares\x18\x02 \x01(\x01\x12\x12\n\nold_shares\x18\x03 \x01(\x01\x12\r\n\x05score\x18\x04 \x01(\x01\x32\x9b\x01\n\rSplitsService\x12\x89\x01\n\x06Splits\x12>.systemathics.apis.services.corporate_actions.v1.SplitsRequest\x1a?.systemathics.apis.services.corporate_actions.v1.SplitsResponseb\x06proto3'
  ,
  dependencies=[google_dot_type_dot_date__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_status__pb2.DESCRIPTOR,])




_SPLITSREQUEST = _descriptor.Descriptor(
  name='SplitsRequest',
  full_name='systemathics.apis.services.corporate_actions.v1.SplitsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='systemathics.apis.services.corporate_actions.v1.SplitsRequest.identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='constraints', full_name='systemathics.apis.services.corporate_actions.v1.SplitsRequest.constraints', index=1,
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
  serialized_start=288,
  serialized_end=437,
)


_SPLITSRESPONSE = _descriptor.Descriptor(
  name='SplitsResponse',
  full_name='systemathics.apis.services.corporate_actions.v1.SplitsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='systemathics.apis.services.corporate_actions.v1.SplitsResponse.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='systemathics.apis.services.corporate_actions.v1.SplitsResponse.status', index=1,
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
  serialized_start=440,
  serialized_end=584,
)


_SPLIT = _descriptor.Descriptor(
  name='Split',
  full_name='systemathics.apis.services.corporate_actions.v1.Split',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='date', full_name='systemathics.apis.services.corporate_actions.v1.Split.date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='new_shares', full_name='systemathics.apis.services.corporate_actions.v1.Split.new_shares', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='old_shares', full_name='systemathics.apis.services.corporate_actions.v1.Split.old_shares', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='systemathics.apis.services.corporate_actions.v1.Split.score', index=3,
      number=4, type=1, cpp_type=5, label=1,
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
  serialized_start=586,
  serialized_end=681,
)

_SPLITSREQUEST.fields_by_name['identifier'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2._IDENTIFIER
_SPLITSREQUEST.fields_by_name['constraints'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2._CONSTRAINTS
_SPLITSRESPONSE.fields_by_name['data'].message_type = _SPLIT
_SPLITSRESPONSE.fields_by_name['status'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_status__pb2._STATUS
_SPLIT.fields_by_name['date'].message_type = google_dot_type_dot_date__pb2._DATE
DESCRIPTOR.message_types_by_name['SplitsRequest'] = _SPLITSREQUEST
DESCRIPTOR.message_types_by_name['SplitsResponse'] = _SPLITSRESPONSE
DESCRIPTOR.message_types_by_name['Split'] = _SPLIT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SplitsRequest = _reflection.GeneratedProtocolMessageType('SplitsRequest', (_message.Message,), {
  'DESCRIPTOR' : _SPLITSREQUEST,
  '__module__' : 'systemathics.apis.services.corporate_actions.v1.splits_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.corporate_actions.v1.SplitsRequest)
  })
_sym_db.RegisterMessage(SplitsRequest)

SplitsResponse = _reflection.GeneratedProtocolMessageType('SplitsResponse', (_message.Message,), {
  'DESCRIPTOR' : _SPLITSRESPONSE,
  '__module__' : 'systemathics.apis.services.corporate_actions.v1.splits_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.corporate_actions.v1.SplitsResponse)
  })
_sym_db.RegisterMessage(SplitsResponse)

Split = _reflection.GeneratedProtocolMessageType('Split', (_message.Message,), {
  'DESCRIPTOR' : _SPLIT,
  '__module__' : 'systemathics.apis.services.corporate_actions.v1.splits_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.corporate_actions.v1.Split)
  })
_sym_db.RegisterMessage(Split)



_SPLITSSERVICE = _descriptor.ServiceDescriptor(
  name='SplitsService',
  full_name='systemathics.apis.services.corporate_actions.v1.SplitsService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=684,
  serialized_end=839,
  methods=[
  _descriptor.MethodDescriptor(
    name='Splits',
    full_name='systemathics.apis.services.corporate_actions.v1.SplitsService.Splits',
    index=0,
    containing_service=None,
    input_type=_SPLITSREQUEST,
    output_type=_SPLITSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SPLITSSERVICE)

DESCRIPTOR.services_by_name['SplitsService'] = _SPLITSSERVICE

# @@protoc_insertion_point(module_scope)
