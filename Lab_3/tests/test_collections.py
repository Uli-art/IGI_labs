import unittest

from ObjectSerializer.Constants import JSON_FORMAT, XML_FORMAT

from ObjectSerializer.SerializerFactory import SerializerFactory

serializer_factory = SerializerFactory()
json_serializer = serializer_factory.create_serializer(JSON_FORMAT)
xml_serializer = serializer_factory.create_serializer(XML_FORMAT)

TUPLE_TEST = (1, "ff", 1.3, {"e": 3})
SET_TEST = {2, "String", False}
DICT_TEST = {"2": "3", "3": [1, 2]}
LIST_TEST = ["String", [1, 2]]


class MyTestCase(unittest.TestCase):
    def test_tuple(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(TUPLE_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(TUPLE_TEST))
        self.assertEqual(TUPLE_TEST, json_decoded, xml_decoded)

    def test_set(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(SET_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(SET_TEST))
        self.assertEqual(SET_TEST, json_decoded, xml_decoded)

    def test_dict(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(DICT_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(DICT_TEST))
        self.assertEqual(DICT_TEST, json_decoded, xml_decoded)

    def test_list(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(LIST_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(LIST_TEST))
        self.assertEqual(LIST_TEST, json_decoded, xml_decoded)


if __name__ == '__main__':
    unittest.main()
