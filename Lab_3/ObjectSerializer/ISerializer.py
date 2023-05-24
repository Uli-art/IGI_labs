from abc import ABC, abstractmethod
from .Constants import EntityTypes


class IObjectEncoder(ABC):
    @abstractmethod
    def encode(self, packed_object) -> str:
        pass


class IObjectDecoder(ABC):
    class Token:
        type: EntityTypes
        value: str
        closure: bool

        def __init__(self, data_type: EntityTypes, value: str, closure: bool):
            self.type = data_type
            self.value = value
            self.closure = closure

    @abstractmethod
    def init(self, source):
        pass

    @abstractmethod
    def get_next_token(self) -> Token:
        pass


class ISerializer(ABC):
    @abstractmethod
    def dump(self, obj, file):
        pass

    @abstractmethod
    def dumps(self, obj):
        pass

    @abstractmethod
    def load(self, file):
        pass

    @abstractmethod
    def loads(self, s):
        pass
