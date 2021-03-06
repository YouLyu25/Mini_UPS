# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: amazon.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='amazon.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x0c\x61mazon.proto\":\n\x08\x41Product\x12\n\n\x02id\x18\x01 \x02(\x03\x12\x13\n\x0b\x64\x65scription\x18\x02 \x02(\t\x12\r\n\x05\x63ount\x18\x03 \x02(\x05\"&\n\x0e\x41InitWarehouse\x12\t\n\x01x\x18\x01 \x02(\x05\x12\t\n\x01y\x18\x02 \x02(\x05\"<\n\x08\x41\x43onnect\x12\x0f\n\x07worldid\x18\x01 \x02(\x03\x12\x1f\n\x06initwh\x18\x02 \x03(\x0b\x32\x0f.AInitWarehouse\"\x1b\n\nAConnected\x12\r\n\x05\x65rror\x18\x01 \x01(\t\"A\n\x05\x41Pack\x12\r\n\x05whnum\x18\x01 \x02(\x05\x12\x19\n\x06things\x18\x02 \x03(\x0b\x32\t.AProduct\x12\x0e\n\x06shipid\x18\x03 \x02(\x03\"=\n\x0b\x41PutOnTruck\x12\r\n\x05whnum\x18\x01 \x02(\x05\x12\x0f\n\x07truckid\x18\x02 \x02(\x05\x12\x0e\n\x06shipid\x18\x03 \x02(\x03\"9\n\rAPurchaseMore\x12\r\n\x05whnum\x18\x01 \x02(\x05\x12\x19\n\x06things\x18\x02 \x03(\x0b\x32\t.AProduct\"\x82\x01\n\tACommands\x12\x1b\n\x03\x62uy\x18\x01 \x03(\x0b\x32\x0e.APurchaseMore\x12\x1a\n\x04load\x18\x02 \x03(\x0b\x32\x0c.APutOnTruck\x12\x16\n\x06topack\x18\x03 \x03(\x0b\x32\x06.APack\x12\x10\n\x08simspeed\x18\x04 \x01(\r\x12\x12\n\ndisconnect\x18\x05 \x01(\x08\"m\n\nAResponses\x12\x1f\n\x07\x61rrived\x18\x01 \x03(\x0b\x32\x0e.APurchaseMore\x12\r\n\x05ready\x18\x02 \x03(\x03\x12\x0e\n\x06loaded\x18\x03 \x03(\x03\x12\r\n\x05\x65rror\x18\x04 \x01(\t\x12\x10\n\x08\x66inished\x18\x05 \x01(\x08')
)




_APRODUCT = _descriptor.Descriptor(
  name='AProduct',
  full_name='AProduct',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='AProduct.id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='AProduct.description', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='AProduct.count', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=16,
  serialized_end=74,
)


_AINITWAREHOUSE = _descriptor.Descriptor(
  name='AInitWarehouse',
  full_name='AInitWarehouse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='AInitWarehouse.x', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='AInitWarehouse.y', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=114,
)


_ACONNECT = _descriptor.Descriptor(
  name='AConnect',
  full_name='AConnect',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='worldid', full_name='AConnect.worldid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='initwh', full_name='AConnect.initwh', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=116,
  serialized_end=176,
)


_ACONNECTED = _descriptor.Descriptor(
  name='AConnected',
  full_name='AConnected',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='AConnected.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=178,
  serialized_end=205,
)


_APACK = _descriptor.Descriptor(
  name='APack',
  full_name='APack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='whnum', full_name='APack.whnum', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='things', full_name='APack.things', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shipid', full_name='APack.shipid', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=207,
  serialized_end=272,
)


_APUTONTRUCK = _descriptor.Descriptor(
  name='APutOnTruck',
  full_name='APutOnTruck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='whnum', full_name='APutOnTruck.whnum', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='truckid', full_name='APutOnTruck.truckid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shipid', full_name='APutOnTruck.shipid', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=274,
  serialized_end=335,
)


_APURCHASEMORE = _descriptor.Descriptor(
  name='APurchaseMore',
  full_name='APurchaseMore',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='whnum', full_name='APurchaseMore.whnum', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='things', full_name='APurchaseMore.things', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=337,
  serialized_end=394,
)


_ACOMMANDS = _descriptor.Descriptor(
  name='ACommands',
  full_name='ACommands',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buy', full_name='ACommands.buy', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='load', full_name='ACommands.load', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='topack', full_name='ACommands.topack', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='simspeed', full_name='ACommands.simspeed', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disconnect', full_name='ACommands.disconnect', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=397,
  serialized_end=527,
)


_ARESPONSES = _descriptor.Descriptor(
  name='AResponses',
  full_name='AResponses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='arrived', full_name='AResponses.arrived', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ready', full_name='AResponses.ready', index=1,
      number=2, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='loaded', full_name='AResponses.loaded', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='AResponses.error', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='finished', full_name='AResponses.finished', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=529,
  serialized_end=638,
)

_ACONNECT.fields_by_name['initwh'].message_type = _AINITWAREHOUSE
_APACK.fields_by_name['things'].message_type = _APRODUCT
_APURCHASEMORE.fields_by_name['things'].message_type = _APRODUCT
_ACOMMANDS.fields_by_name['buy'].message_type = _APURCHASEMORE
_ACOMMANDS.fields_by_name['load'].message_type = _APUTONTRUCK
_ACOMMANDS.fields_by_name['topack'].message_type = _APACK
_ARESPONSES.fields_by_name['arrived'].message_type = _APURCHASEMORE
DESCRIPTOR.message_types_by_name['AProduct'] = _APRODUCT
DESCRIPTOR.message_types_by_name['AInitWarehouse'] = _AINITWAREHOUSE
DESCRIPTOR.message_types_by_name['AConnect'] = _ACONNECT
DESCRIPTOR.message_types_by_name['AConnected'] = _ACONNECTED
DESCRIPTOR.message_types_by_name['APack'] = _APACK
DESCRIPTOR.message_types_by_name['APutOnTruck'] = _APUTONTRUCK
DESCRIPTOR.message_types_by_name['APurchaseMore'] = _APURCHASEMORE
DESCRIPTOR.message_types_by_name['ACommands'] = _ACOMMANDS
DESCRIPTOR.message_types_by_name['AResponses'] = _ARESPONSES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AProduct = _reflection.GeneratedProtocolMessageType('AProduct', (_message.Message,), dict(
  DESCRIPTOR = _APRODUCT,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:AProduct)
  ))
_sym_db.RegisterMessage(AProduct)

AInitWarehouse = _reflection.GeneratedProtocolMessageType('AInitWarehouse', (_message.Message,), dict(
  DESCRIPTOR = _AINITWAREHOUSE,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:AInitWarehouse)
  ))
_sym_db.RegisterMessage(AInitWarehouse)

AConnect = _reflection.GeneratedProtocolMessageType('AConnect', (_message.Message,), dict(
  DESCRIPTOR = _ACONNECT,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:AConnect)
  ))
_sym_db.RegisterMessage(AConnect)

AConnected = _reflection.GeneratedProtocolMessageType('AConnected', (_message.Message,), dict(
  DESCRIPTOR = _ACONNECTED,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:AConnected)
  ))
_sym_db.RegisterMessage(AConnected)

APack = _reflection.GeneratedProtocolMessageType('APack', (_message.Message,), dict(
  DESCRIPTOR = _APACK,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:APack)
  ))
_sym_db.RegisterMessage(APack)

APutOnTruck = _reflection.GeneratedProtocolMessageType('APutOnTruck', (_message.Message,), dict(
  DESCRIPTOR = _APUTONTRUCK,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:APutOnTruck)
  ))
_sym_db.RegisterMessage(APutOnTruck)

APurchaseMore = _reflection.GeneratedProtocolMessageType('APurchaseMore', (_message.Message,), dict(
  DESCRIPTOR = _APURCHASEMORE,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:APurchaseMore)
  ))
_sym_db.RegisterMessage(APurchaseMore)

ACommands = _reflection.GeneratedProtocolMessageType('ACommands', (_message.Message,), dict(
  DESCRIPTOR = _ACOMMANDS,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:ACommands)
  ))
_sym_db.RegisterMessage(ACommands)

AResponses = _reflection.GeneratedProtocolMessageType('AResponses', (_message.Message,), dict(
  DESCRIPTOR = _ARESPONSES,
  __module__ = 'amazon_pb2'
  # @@protoc_insertion_point(class_scope:AResponses)
  ))
_sym_db.RegisterMessage(AResponses)


# @@protoc_insertion_point(module_scope)
