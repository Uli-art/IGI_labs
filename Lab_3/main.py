import math
from ObjectSerializer.Constants import JSON_FORMAT, XML_FORMAT
from ObjectSerializer.SerializerFactory import SerializerFactory

serializer_factory = SerializerFactory()
json_serializer = serializer_factory.create_serializer(JSON_FORMAT)
xml_serializer = serializer_factory.create_serializer(XML_FORMAT)


def my_decor(meth):
    def inner(*args, **kwargs):
        print('I am in my_decor')
        return meth(*args, **kwargs)

    return inner


class A:
    x = 10

    @my_decor
    def my_sin(self, c):
        return math.sin(c * self.x)

    @staticmethod
    def stat():
        return 145

    def __str__(self):
        return 'AAAAA'

    def __repr__(self):
        return 'AAAAA'


class B:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def prop(self):
        return self.a * self.b

    @classmethod
    def class_meth(cls):
        return math.pi


class C(A, B):
    pass


if __name__ == '__main__':

    # var = 15
    # var_ser = ser.dumps(var)
    # var_des = ser.loads(var_ser)
    # print(var_des)

    C_ser = json_serializer.dumps(C)
    C_des = json_serializer.loads(C_ser)

    c = C(1, 2)
    c_ser = json_serializer.dumps(c)
    c_des = json_serializer.loads(c_ser)

    print(c_des)
    print(c_des.x)
    print(c_des.my_sin(10))
    print(c_des.prop)
    print(C_des.stat())
    print(c_des.class_meth())
    print()
    print(c)
    print(c.x)
    print(c.my_sin(10))
    print(c.prop)
    print(C.stat())
    print(c.class_meth())
