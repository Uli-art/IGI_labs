import base64
import inspect

from . import Util
from .Constants import EntityTypes, PARAMS_FOR_CODE_REPLACE, NONSERIALIZABLE_TYPES, UNSERIALIZABLE_DUNDER
from types import FunctionType, CodeType, CellType, MethodType, ModuleType


def object_type_to_entity_type(obj):
    if isinstance(obj, type(None)):
        return EntityTypes.NONE

    if isinstance(obj, bool):
        return EntityTypes.BOOL

    if isinstance(obj, int):
        return EntityTypes.INT

    if isinstance(obj, float):
        return EntityTypes.FLOAT

    if isinstance(obj, str):
        return EntityTypes.STRING

    if isinstance(obj, tuple):
        return EntityTypes.TUPLE

    if isinstance(obj, list):
        return EntityTypes.LIST

    if isinstance(obj, set):
        return EntityTypes.SET

    if isinstance(obj, dict):
        return EntityTypes.DICT

    if isinstance(obj, bytes):
        return EntityTypes.BYTES

    if isinstance(obj, ModuleType):
        return EntityTypes.MODULE

    if Util.is_iterator(obj):
        return EntityTypes.ITERATOR

    if isinstance(obj, FunctionType) or isinstance(obj, MethodType):
        return EntityTypes.FUNCTION

    if isinstance(obj, CellType):
        return EntityTypes.CELL

    if isinstance(obj, CodeType):
        return EntityTypes.CODE

    if Util.is_class(obj):
        return EntityTypes.CLASS

    if Util.is_object(obj):
        return EntityTypes.OBJECT

    return None


class PythonEntity:
    entity_type = EntityTypes.UNDEFINED
    content = None

    def __init__(self, entity_type: EntityTypes, content):
        self.entity_type = entity_type
        self.content = content


def pack_python_object(obj) -> PythonEntity:
    entity_type = object_type_to_entity_type(obj)

    if Util.is_primitive(obj) | Util.is_dict(obj):
        return PythonEntity(entity_type, obj)
    elif Util.is_sequence(obj):
        return PythonEntity(entity_type, obj) if isinstance(obj, list) else pack_to_dict(entity_type, list(obj))
    elif Util.is_bytes(obj):
        return pack_to_dict(EntityTypes.BYTES, base64.b64encode(obj).decode("ascii"))
    elif Util.is_iterator(obj):
        return pack_to_dict(EntityTypes.ITERATOR, list(obj))
    elif Util.is_module(obj):
        return pack_to_dict(EntityTypes.MODULE, obj.__name__)
    elif Util.is_function(obj):
        return pack_to_dict(entity_type, dict(
            code=obj.__code__,
            globals=dict(zip([attr for attr in obj.__globals__.keys()
                              if attr in obj.__code__.co_names and attr != obj.__code__.co_name],
                              [obj.__globals__[attr] for attr in obj.__globals__.keys()
                              if attr in obj.__code__.co_names and attr != obj.__code__.co_name])),
            name=obj.__name__,
            argdefs=obj.__defaults__,
            closure=obj.__closure__
        ))
    elif Util.is_cell(obj):
        return pack_to_dict(entity_type, obj.cell_contents)
    elif Util.is_code(obj):
        return pack_to_dict(entity_type,
                            dict(zip([attr for attr in dir(obj) if attr in PARAMS_FOR_CODE_REPLACE],
                                     [getattr(obj, attr) for attr in dir(obj) if attr in PARAMS_FOR_CODE_REPLACE])))
    elif Util.is_class(obj):
        return pack_to_dict(entity_type, dict(
            name=obj.__name__,
            bases=tuple(attr for attr in obj.__bases__ if attr != object),
            dict={attr: getattr(obj, attr) for attr, value in inspect.getmembers(obj)
                  if attr not in UNSERIALIZABLE_DUNDER
                  and type(value) not in NONSERIALIZABLE_TYPES}
        ))
    elif Util.is_object(obj):
        return pack_to_dict(entity_type, dict(
            base_class=obj.__class__,
            attributes={attr: value
                        for attr, value in inspect.getmembers(obj)
                        if not attr.startswith('__')
                        and not Util.is_function(value)}
        ))

    return PythonEntity(EntityTypes.NONE, None)


def pack_to_dict(entity_type, obj):
    return PythonEntity(EntityTypes.DICT, {f"{EntityTypes.__name__}.{entity_type.name}": obj})


def unpack_python_object(packed_entity: PythonEntity):
    match packed_entity.entity_type:
        case EntityTypes.FUNCTION:
            return FunctionType(**packed_entity.content)
        case EntityTypes.CELL:
            content = packed_entity.content
            return (lambda: content).__closure__[0]
        case EntityTypes.CODE:
            def default():
                pass
            return default.__code__.replace(**packed_entity.content)
        case EntityTypes.CLASS:
            obj = type(packed_entity.content['name'], packed_entity.content['bases'], packed_entity.content['dict'])
            return obj
        case EntityTypes.OBJECT:
            obj = object.__new__(packed_entity.content['base_class'])
            obj.__dict__=packed_entity.content['attributes']
            return obj
        case EntityTypes.ITERATOR:
            return iter([item for item in packed_entity.content])
        case EntityTypes.BYTES:
            return base64.b64decode(packed_entity.content)
        case EntityTypes.TUPLE:
            return tuple(packed_entity.content)
        case EntityTypes.SET:
            return set(packed_entity.content)
        case EntityTypes.MODULE:
            return __import__(packed_entity.content)

    return packed_entity.content
