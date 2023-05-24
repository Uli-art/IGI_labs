import enum

from .ISerializer import ISerializer
from .JsonBackend import JsonEncoder, JsonDecoder
from .XmlBackend import XmlEncoder, XmlDecoder
from .BaseSerializer import BaseSerializer
from .Constants import JSON_FORMAT, XML_FORMAT, YAML_FORMAT, TOML_FORMAT


class UnknownFormat(Exception):
    pass


class NotImplementedFormat(Exception):
    pass


class SerializerFactory:
    @classmethod
    def create_serializer(cls, serializer_format: str) -> ISerializer:
        fmt = serializer_format.lower()

        if fmt == JSON_FORMAT:
            return BaseSerializer(JsonEncoder(), JsonDecoder())
        elif fmt == XML_FORMAT:
            return BaseSerializer(XmlEncoder(), XmlDecoder())
        elif fmt == YAML_FORMAT:
            raise NotImplementedFormat()
        elif fmt == TOML_FORMAT:
            raise NotImplementedFormat()

        raise UnknownFormat()
