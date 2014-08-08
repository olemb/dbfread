from .field_parser import InvalidValue

assert repr(InvalidValue(b'')) == "InvalidValue(b'')"
