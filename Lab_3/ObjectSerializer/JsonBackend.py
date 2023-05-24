import re

from .ISerializer import IObjectEncoder, IObjectDecoder
from .PythonEntityPacker import pack_python_object
from .Constants import EntityTypes


class JsonEncoder(IObjectEncoder):
    def encode(self, obj) -> str:
        packed_object = pack_python_object(obj);
        if packed_object.entity_type in (EntityTypes.NONE,
                                         EntityTypes.INT,
                                         EntityTypes.FLOAT,
                                         EntityTypes.BOOL,
                                         EntityTypes.STRING):
            return self.encode_primitive(packed_object)
        elif packed_object.entity_type == EntityTypes.LIST:
            return self.encode_list(packed_object)
        elif packed_object.entity_type == EntityTypes.DICT:
            return self.encode_dict(packed_object)

        raise NotImplemented()

    def encode_primitive(self, packed_object):
        if packed_object.entity_type == EntityTypes.STRING:
            return "\"{value}\"".format(value=packed_object.content)
        return str(packed_object.content).lower() if packed_object.content is not None else "null"

    def encode_list(self, packed_object):
        return "[" + ", ".join([self.encode(val) for val in packed_object.content]) + "]"

    def encode_dict(self, packed_object):
        return "{" + ", ".join(["\"{key}\": {value}".format(key=key, value=self.encode(val))
                                for (key, val) in packed_object.content.items()]) + "}"


class JsonDecoder(IObjectDecoder):
    json: str
    current_position: int
    end_position: int

    def init(self, source):
        self.json = source
        self.current_position = 0
        self.end_position = len(self.json)

    def get_next_token(self) -> IObjectDecoder.Token:
        next_token = IObjectDecoder.Token(EntityTypes.UNDEFINED, "", True)

        if self.current_position >= self.end_position:
            return next_token

        while self.current_position < self.end_position:
            next_char = self.json[self.current_position]

            if next_char.isspace() or next_char in (',', ':'):
                self.current_position += 1
                if len(next_token.value) > 0:
                    break
                else:
                    continue

            if next_char in ('[', '{', '}', ']', '\"'):
                if len(next_token.value) > 0:
                    break

            self.current_position += 1
            next_token.value += next_char

            match next_char:
                case '[':
                    next_token.type = EntityTypes.LIST
                    next_token.closure = False
                    break
                case ']':
                    next_token.type = EntityTypes.LIST
                    next_token.closure = True
                    break
                case '{':
                    next_token.type = EntityTypes.DICT
                    next_token.closure = False
                    break
                case '}':
                    next_token.type = EntityTypes.DICT
                    next_token.closure = True
                    break
                case '\"':
                    match = re.match("^\"([^\"]*)\"", self.json[self.current_position - 1:])
                    if match is not None:
                        next_token.type = EntityTypes.STRING
                        next_token.value = match.group(1)

                        self.current_position += len(next_token.value) + 1
                        break

                    return IObjectDecoder.Token(EntityTypes.UNDEFINED, "", True)

        if next_token.type == EntityTypes.UNDEFINED:
            if not next_token.value or next_token.value == 'null':
                next_token.type = EntityTypes.NONE
            elif re.fullmatch("true|false", next_token.value) is not None:
                next_token.type = EntityTypes.BOOL
            elif re.fullmatch("[0-9]+", next_token.value) is not None:
                next_token.type = EntityTypes.INT
            elif re.fullmatch("[0-9]*.[0-9]+", next_token.value) is not None:
                next_token.type = EntityTypes.FLOAT

        return next_token
