from .ISerializer import IObjectEncoder, IObjectDecoder
from .PythonEntityPacker import pack_python_object
from .Constants import EntityTypes
from .Util import xml_escape, xml_unescape

class XmlEncoder(IObjectEncoder):
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
        value = xml_escape(packed_object.content) if packed_object.entity_type == EntityTypes.STRING \
            else packed_object.content
        return "<{type}>{value}</{type}>".format(
             type=packed_object.entity_type.name.lower(), value=value)

    def encode_list(self, packed_object):
        return "<list>" + ''.join(["{value}".format(value=self.encode(item))
                          for item in packed_object.content]) + "</list>"

    def encode_dict(self, packed_object):
        return "<dict>" + ''.join(["{key}{value}".format(key=self.encode(key), value=self.encode(value))
                                   for (key, value) in packed_object.content.items()]) + "</dict>"


class XmlDecoder(IObjectDecoder):
    xml: str
    current_position: int
    end_position: int

    def init(self, source):
        self.xml = source
        self.current_position = 0
        self.end_position = len(self.xml)

    def get_next_token(self) -> IObjectDecoder.Token:
        result, xml_tag_name, closure = self.read_xml_tag()

        if  result:
            match xml_tag_name:
                case 'list':
                    return IObjectDecoder.Token(EntityTypes.LIST, xml_tag_name, closure)
                case 'dict':
                    return IObjectDecoder.Token(EntityTypes.DICT, xml_tag_name, closure)
                case 'none':
                    return self.read_none()
                case 'bool':
                    return self.read_bool()
                case 'int':
                    return self.read_int()
                case 'float':
                    return self.read_float()
                case 'string':
                    return self.read_string()

        return IObjectDecoder.Token(EntityTypes.UNDEFINED, "", True)

    def read_xml_tag(self):
        next_char = ''
        while self.current_position < self.end_position:
            next_char = self.read_next_char()
            if next_char == '<':
                 break

        if next_char != '<':
            return False, next_char, True

        xml_tag_name = ''
        closure = False
        while self.current_position < self.end_position:
            next_char = self.read_next_char()
            if next_char == '/':
                closure = True
                continue
            elif next_char == '>':
                 break
            xml_tag_name += next_char

        return True, xml_tag_name, closure

    def read_value(self):
        value = ''
        while (self.current_position < self.end_position) and self.xml[self.current_position] != '<':
            value += self.read_next_char()

        return xml_unescape(value)

    def read_next_char(self):
        next_char = self.xml[self.current_position]
        self.current_position += 1

        return next_char

    def read_none(self):
        self.current_position += len('None</none>')
        return IObjectDecoder.Token(EntityTypes.NONE, "None", True)

    def read_bool(self):
        value = self.read_value()
        self.current_position += len('</bool>')
        return IObjectDecoder.Token(EntityTypes.BOOL, value, True)

    def read_int(self):
        value = self.read_value()
        self.current_position += len('</int>')
        return IObjectDecoder.Token(EntityTypes.INT, value, True)

    def read_float(self):
        value = self.read_value()
        self.current_position += len('</float>')
        return IObjectDecoder.Token(EntityTypes.FLOAT, value, True)

    def read_string(self):
        value = self.read_value()
        self.current_position += len('</string>')
        return IObjectDecoder.Token(EntityTypes.STRING, value, True)
