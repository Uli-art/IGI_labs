import math
import unittest
from ObjectSerializer.Constants import JSON_FORMAT, XML_FORMAT

from ObjectSerializer.SerializerFactory import SerializerFactory

serializer_factory = SerializerFactory()
json_serializer = serializer_factory.create_serializer(JSON_FORMAT)
xml_serializer = serializer_factory.create_serializer(XML_FORMAT)

iterator = iter([1, 2, 3])

class SimpleClass:
    a = 3
    b = "String"


class ClassWithStaticMethods:
    a = 3
    b = "String"

    @staticmethod
    def static_method():
        return "Static method"


class ClassWithClassMethods:
    a = 3
    b = "String"

    @classmethod
    def class_method(cls):
        return cls.b + str(cls.a)


class Class1:
    x = 2
    y = 3

    def method(self):
        return "Method in Class1"

    def get_sum(self):
        return self.x + self.y


class Class2Mro(Class1):
    def method(self):
        return "Method in Class2"


class Class3:
    a = "String"

    @staticmethod
    def get_pi():
        return math.pi


class Class4(Class1, Class3):
    pass


class Class5(Class1):
    pass


class Class6(Class5):
    @staticmethod
    def method3():
        return "Class6 method"


class Class7(Class6):
    pass


class MyTestCase(unittest.TestCase):
    def test_simple_class(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(SimpleClass))

        self.assertEqual(SimpleClass.a, json_decoded.a)
        self.assertEqual(SimpleClass.b, json_decoded.b)

    def test_inheritance(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(Class4))

        self.assertEqual(Class4().method(), json_decoded().method())
        self.assertEqual(Class4.get_pi(), json_decoded.get_pi())

    def test_multy_inheritance(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(Class7))

        self.assertEqual(Class7().method(), json_decoded().method())
        self.assertEqual(Class7.method3(), json_decoded.method3())

    def test_static_methods(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(ClassWithStaticMethods))

        self.assertEqual(ClassWithStaticMethods.static_method(), json_decoded.static_method())

    def test_class_methods(self):
        result = json_serializer.dumps(ClassWithClassMethods)
        json_decoded = json_serializer.loads(json_serializer.dumps(ClassWithClassMethods))

        self.assertEqual(ClassWithClassMethods().class_method(), json_decoded().class_method())

    def test_mro(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(Class2Mro))

        self.assertEqual(Class2Mro().method(), json_decoded().method())

    def test_iterator(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(iterator))

        self.assertEqual([1, 2, 3], list(json_decoded))


if __name__ == '__main__':
    unittest.main()
