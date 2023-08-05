# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/services/corporate_actions/v1/changes.proto
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
  name='systemathics/apis/services/corporate_actions/v1/changes.proto',
  package='systemathics.apis.services.corporate_actions.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n=systemathics/apis/services/corporate_actions/v1/changes.proto\x12/systemathics.apis.services.corporate_actions.v1\x1a\x16google/type/date.proto\x1a\x31systemathics/apis/type/shared/v1/identifier.proto\x1a\x32systemathics/apis/type/shared/v1/constraints.proto\x1a-systemathics/apis/type/shared/v1/status.proto\"\x96\x01\n\x0e\x43hangesRequest\x12@\n\nidentifier\x18\x01 \x01(\x0b\x32,.systemathics.apis.type.shared.v1.Identifier\x12\x42\n\x0b\x63onstraints\x18\x02 \x01(\x0b\x32-.systemathics.apis.type.shared.v1.Constraints\"\x92\x01\n\x0f\x43hangesResponse\x12\x45\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x37.systemathics.apis.services.corporate_actions.v1.Change\x12\x38\n\x06status\x18\x02 \x01(\x0b\x32(.systemathics.apis.type.shared.v1.Status\"`\n\x06\x43hange\x12\x1f\n\x04\x64\x61te\x18\x01 \x01(\x0b\x32\x11.google.type.Date\x12\x12\n\nnew_symbol\x18\x02 \x01(\t\x12\x12\n\nold_symbol\x18\x03 \x01(\t\x12\r\n\x05score\x18\x04 \x01(\x01\x32\x9f\x01\n\x0e\x43hangesService\x12\x8c\x01\n\x07\x43hanges\x12?.systemathics.apis.services.corporate_actions.v1.ChangesRequest\x1a@.systemathics.apis.services.corporate_actions.v1.ChangesResponseb\x06proto3'
  ,
  dependencies=[google_dot_type_dot_date__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_status__pb2.DESCRIPTOR,])




_CHANGESREQUEST = _descriptor.Descriptor(
  name='ChangesRequest',
  full_name='systemathics.apis.services.corporate_actions.v1.ChangesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='systemathics.apis.services.corporate_actions.v1.ChangesRequest.identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='constraints', full_name='systemathics.apis.services.corporate_actions.v1.ChangesRequest.constraints', index=1,
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
  serialized_start=289,
  serialized_end=439,
)


_CHANGESRESPONSE = _descriptor.Descriptor(
  name='ChangesResponse',
  full_name='systemathics.apis.services.corporate_actions.v1.ChangesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='systemathics.apis.services.corporate_actions.v1.ChangesResponse.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='systemathics.apis.services.corporate_actions.v1.ChangesResponse.status', index=1,
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
  serialized_start=442,
  serialized_end=588,
)


_CHANGE = _descriptor.Descriptor(
  name='Change',
  full_name='systemathics.apis.services.corporate_actions.v1.Change',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='date', full_name='systemathics.apis.services.corporate_actions.v1.Change.date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='new_symbol', full_name='systemathics.apis.services.corporate_actions.v1.Change.new_symbol', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='old_symbol', full_name='systemathics.apis.services.corporate_actions.v1.Change.old_symbol', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='systemathics.apis.services.corporate_actions.v1.Change.score', index=3,
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
  serialized_start=590,
  serialized_end=686,
)

_CHANGESREQUEST.fields_by_name['identifier'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2._IDENTIFIER
_CHANGESREQUEST.fields_by_name['constraints'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_constraints__pb2._CONSTRAINTS
_CHANGESRESPONSE.fields_by_name['data'].message_type = _CHANGE
_CHANGESRESPONSE.fields_by_name['status'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_status__pb2._STATUS
_CHANGE.fields_by_name['date'].message_type = google_dot_type_dot_date__pb2._DATE
DESCRIPTOR.message_types_by_name['ChangesRequest'] = _CHANGESREQUEST
DESCRIPTOR.message_types_by_name['ChangesResponse'] = _CHANGESRESPONSE
DESCRIPTOR.message_types_by_name['Change'] = _CHANGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ChangesRequest = _reflection.GeneratedProtocolMessageType('ChangesRequest', (_message.Message,), {
  'DESCRIPTOR' : _CHANGESREQUEST,
  '__module__' : 'systemathics.apis.services.corporate_actions.v1.changes_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.corporate_actions.v1.ChangesRequest)
  })
_sym_db.RegisterMessage(ChangesRequest)

ChangesResponse = _reflection.GeneratedProtocolMessageType('ChangesResponse', (_message.Message,), {
  'DESCRIPTOR' : _CHANGESRESPONSE,
  '__module__' : 'systemathics.apis.services.corporate_actions.v1.changes_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.corporate_actions.v1.ChangesResponse)
  })
_sym_db.RegisterMessage(ChangesResponse)

Change = _reflection.GeneratedProtocolMessageType('Change', (_message.Message,), {
  'DESCRIPTOR' : _CHANGE,
  '__module__' : 'systemathics.apis.services.corporate_actions.v1.changes_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.services.corporate_actions.v1.Change)
  })
_sym_db.RegisterMessage(Change)



_CHANGESSERVICE = _descriptor.ServiceDescriptor(
  name='ChangesService',
  full_name='systemathics.apis.services.corporate_actions.v1.ChangesService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=689,
  serialized_end=848,
  methods=[
  _descriptor.MethodDescriptor(
    name='Changes',
    full_name='systemathics.apis.services.corporate_actions.v1.ChangesService.Changes',
    index=0,
    containing_service=None,
    input_type=_CHANGESREQUEST,
    output_type=_CHANGESRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CHANGESSERVICE)

DESCRIPTOR.services_by_name['ChangesService'] = _CHANGESSERVICE

# @@protoc_insertion_point(module_scope)
