# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: systemathics/apis/type/shared/v1/level.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='systemathics/apis/type/shared/v1/level.proto',
  package='systemathics.apis.type.shared.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n,systemathics/apis/type/shared/v1/level.proto\x12 systemathics.apis.type.shared.v1*K\n\x05Level\x12\x15\n\x11LEVEL_UNSPECIFIED\x10\x00\x12\x10\n\x0cLEVEL_TRADES\x10\x01\x12\x19\n\x15LEVEL_TRADES_AND_BOOK\x10\x02\x62\x06proto3'
)

_LEVEL = _descriptor.EnumDescriptor(
  name='Level',
  full_name='systemathics.apis.type.shared.v1.Level',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LEVEL_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LEVEL_TRADES', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LEVEL_TRADES_AND_BOOK', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=82,
  serialized_end=157,
)
_sym_db.RegisterEnumDescriptor(_LEVEL)

Level = enum_type_wrapper.EnumTypeWrapper(_LEVEL)
LEVEL_UNSPECIFIED = 0
LEVEL_TRADES = 1
LEVEL_TRADES_AND_BOOK = 2


DESCRIPTOR.enum_types_by_name['Level'] = _LEVEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


# @@protoc_insertion_point(module_scope)
