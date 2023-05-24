import math
import unittest

from ObjectSerializer.Constants import JSON_FORMAT, XML_FORMAT

from ObjectSerializer.SerializerFactory import SerializerFactory

serializer_factory = SerializerFactory()
json_serializer = serializer_factory.create_serializer(JSON_FORMAT)
xml_serializer = serializer_factory.create_serializer(XML_FORMAT)


def simple_function(x, y):
    return x**2 + y**2


lambda_function = lambda x: x**2


def fibonacci(x):
    if x >= 1:
        return 1
    return fibonacci(x - 1) + fibonacci(x - 2)


def generators():
    for i in range(5):
        yield i


def inner_generators():
    for i in range(5):
        yield i
    yield from generators()


def outer_function():
    value = 0

    def inner_function():
        nonlocal value
        value += 5
    return inner_function


def decorator(function):
    def wrappers(*args, **kwargs):
        value = function(*args, **kwargs)
        value += 5
        return value
    return wrappers


@decorator
def decorated(x):
    return x**2


GLOBAL_VALUE = "fff"


def function_with_global():
    return GLOBAL_VALUE + "get global"


class MyTestCase(unittest.TestCase):
    def test_simple_function(self):
        x, y = 2, 3
        json_decoded = json_serializer.loads(json_serializer.dumps(simple_function))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(simple_function))
        self.assertEqual(simple_function(x, y), json_decoded(x, y), xml_decoded(x, y))

    def test_recursion(self):
        x = 5
        json_decoded = json_serializer.loads(json_serializer.dumps(fibonacci))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(fibonacci))
        self.assertEqual(fibonacci(x), json_decoded(x), xml_decoded(x))

    def test_lambda(self):
        x = 3
        json_decoded = json_serializer.loads(json_serializer.dumps(lambda_function))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(lambda_function))
        self.assertEqual(lambda_function(x), json_decoded(x), xml_decoded(x))

    def test_closures(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(outer_function))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(outer_function))
        self.assertEqual(outer_function()(), json_decoded()(), xml_decoded()())

    # def test_iterators(self):
    #     json_decoded = json_serializer.loads(json_serializer.dumps(TUPLE_TEST))
    #
    #     self.assertEqual(TUPLE_TEST, json_decoded)

    def test_generators(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(generators))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(generators))
        self.assertEqual([*generators()], [*json_decoded()], [*xml_decoded()])

    def test_inner_generators(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(inner_generators))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(inner_generators))
        self.assertEqual([*inner_generators()], [*json_decoded()], [*xml_decoded()])

    def test_wrappers(self):
        x = 6
        json_decoded = json_serializer.loads(json_serializer.dumps(decorator))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(decorator))
        self.assertEqual(decorator(decorated)(x), json_decoded(decorated)(x), xml_decoded(decorated)(x))

    def test_functions_with_globals(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(function_with_global))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(function_with_global))
        self.assertEqual(function_with_global(), json_decoded(), xml_decoded())


if __name__ == '__main__':
    unittest.main()
