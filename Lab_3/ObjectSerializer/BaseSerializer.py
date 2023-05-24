import enum

from .Util import is_dict, is_collection
from .ISerializer import ISerializer, IObjectDecoder, IObjectEncoder
from .PythonEntityPacker import pack_python_object, unpack_python_object, PythonEntity
from .Constants import EntityTypes


class BaseSerializer(ISerializer):
    object_encoder: IObjectEncoder
    object_decoder: IObjectDecoder

    def __init__(self, encoder: IObjectEncoder, decoder: IObjectDecoder):
        self.object_encoder = encoder
        self.object_decoder = decoder

    def dump(self, obj, file):
        file.write(self.dumps(obj))

    def dumps(self, obj):
        return self.object_encoder.encode(obj)

    def load(self, file):
        return self.loads(file.read())

    def loads(self, s):

        class CollectionContext:
            collection: object
            key: object

            def __init__(self, collection):
                self.collection = collection
                self.key = None

            def set_value(self, value: object):
                if is_dict(self.collection):
                    if self.key is None:
                        self.key = value
                    else:
                        assert(self.key is not None)
                        self.collection[self.key] = value
                        self.key = None
                else:
                    if isinstance(self.collection, tuple):
                        temp_list = list(self.collection)
                        temp_list.append(value)
                        self.collection = tuple(temp_list)
                    elif isinstance(self.collection, set):
                        self.collection.add(value)
                    else:
                        self.collection.append(value)

        context_stack = list()
        context = CollectionContext(list())

        self.object_decoder.init(s)

        while True:
            next_token = self.object_decoder.get_next_token()
            # print(f"Next token: {next_token.type}, {next_token.value}, {next_token.closure}")

            if next_token.type == EntityTypes.UNDEFINED:
                break

            obj = None
            match next_token.type:
                case EntityTypes.NONE:
                    obj = None
                case EntityTypes.INT:
                    obj = int(next_token.value)
                case EntityTypes.FLOAT:
                    obj = float(next_token.value)
                case EntityTypes.BOOL:
                    obj = True if next_token.value in ("true", "1") else False
                case EntityTypes.STRING:
                    obj = str(next_token.value)
                case EntityTypes.LIST:
                    obj = list() if not next_token.closure else context.collection
                case EntityTypes.TUPLE:
                    obj = tuple() if not next_token.closure else context.collection
                case EntityTypes.SET:
                    obj = set() if not next_token.closure else context.collection
                case EntityTypes.DICT:
                    obj = dict() if not next_token.closure else context.collection

            if is_collection(obj):
                if next_token.closure:
                    assert(context.collection == obj)
                    context = context_stack.pop()
                    # print(f"Close Collection {type(obj)}")
                else:
                    context_stack.append(context)
                    context = CollectionContext(obj)
                    # print(f"Open Collection {type(obj)}")

            if next_token.closure:
                if next_token.type == EntityTypes.DICT:
                    keys = list(obj.keys())
                    if len(keys) == 1 and str(keys[0]).startswith(f"{EntityTypes.__name__}."):
                        entity_type_dict_key = keys[0]
                        entity_type_name = entity_type_dict_key[entity_type_dict_key.index(".") + 1:]
                        obj = unpack_python_object(PythonEntity(EntityTypes[entity_type_name],
                                                                obj[entity_type_dict_key]))

                context.set_value(obj)

        assert(len(context_stack) == 0)
        assert(context is not None and isinstance(context.collection, list))

        return context.collection.pop() if len(context.collection) > 0 else None
