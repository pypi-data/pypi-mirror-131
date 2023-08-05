# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/type/shared/v1/mappings.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from systemathics.apis.type.shared.v1 import identifier_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2
from systemathics.apis.type.shared.v1 import memo_pb2 as systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_memo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='systemathics/apis/type/shared/v1/mappings.proto',
  package='systemathics.apis.type.shared.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n/systemathics/apis/type/shared/v1/mappings.proto\x12 systemathics.apis.type.shared.v1\x1a\x31systemathics/apis/type/shared/v1/identifier.proto\x1a+systemathics/apis/type/shared/v1/memo.proto\"\x97\x01\n\x07Mapping\x12@\n\nidentifier\x18\x01 \x01(\x0b\x32,.systemathics.apis.type.shared.v1.Identifier\x12\x34\n\x04memo\x18\x02 \x01(\x0b\x32&.systemathics.apis.type.shared.v1.Memo\x12\x14\n\x0c\x65vent_source\x18\x03 \x01(\r\"D\n\x08Mappings\x12\x38\n\x05table\x18\x01 \x03(\x0b\x32).systemathics.apis.type.shared.v1.Mappingb\x06proto3'
  ,
  dependencies=[systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2.DESCRIPTOR,systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_memo__pb2.DESCRIPTOR,])




_MAPPING = _descriptor.Descriptor(
  name='Mapping',
  full_name='systemathics.apis.type.shared.v1.Mapping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='systemathics.apis.type.shared.v1.Mapping.identifier', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='memo', full_name='systemathics.apis.type.shared.v1.Mapping.memo', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='event_source', full_name='systemathics.apis.type.shared.v1.Mapping.event_source', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=182,
  serialized_end=333,
)


_MAPPINGS = _descriptor.Descriptor(
  name='Mappings',
  full_name='systemathics.apis.type.shared.v1.Mappings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='table', full_name='systemathics.apis.type.shared.v1.Mappings.table', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=335,
  serialized_end=403,
)

_MAPPING.fields_by_name['identifier'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_identifier__pb2._IDENTIFIER
_MAPPING.fields_by_name['memo'].message_type = systemathics_dot_apis_dot_type_dot_shared_dot_v1_dot_memo__pb2._MEMO
_MAPPINGS.fields_by_name['table'].message_type = _MAPPING
DESCRIPTOR.message_types_by_name['Mapping'] = _MAPPING
DESCRIPTOR.message_types_by_name['Mappings'] = _MAPPINGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Mapping = _reflection.GeneratedProtocolMessageType('Mapping', (_message.Message,), {
  'DESCRIPTOR' : _MAPPING,
  '__module__' : 'systemathics.apis.type.shared.v1.mappings_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.type.shared.v1.Mapping)
  })
_sym_db.RegisterMessage(Mapping)

Mappings = _reflection.GeneratedProtocolMessageType('Mappings', (_message.Message,), {
  'DESCRIPTOR' : _MAPPINGS,
  '__module__' : 'systemathics.apis.type.shared.v1.mappings_pb2'
  # @@protoc_insertion_point(class_scope:systemathics.apis.type.shared.v1.Mappings)
  })
_sym_db.RegisterMessage(Mappings)


# @@protoc_insertion_point(module_scope)
