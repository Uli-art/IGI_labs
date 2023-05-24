import unittest

from ObjectSerializer.Constants import JSON_FORMAT, XML_FORMAT

from ObjectSerializer.SerializerFactory import SerializerFactory

serializer_factory = SerializerFactory()
json_serializer = serializer_factory.create_serializer(JSON_FORMAT)
xml_serializer = serializer_factory.create_serializer(XML_FORMAT)

BOOL_TEST = True
INT_TEST = 3
FLOAT_TEST = 1.5
STRING_TEST = "String"
NONE_TEST = None

class MyTestCase(unittest.TestCase):

    def test_bool(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(BOOL_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(BOOL_TEST))
        self.assertEqual(BOOL_TEST, json_decoded, xml_decoded)

    def test_int(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(INT_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(INT_TEST))
        self.assertEqual(INT_TEST, json_decoded, xml_decoded)

    def test_float(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(FLOAT_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(FLOAT_TEST))
        self.assertEqual(FLOAT_TEST, json_decoded, xml_decoded)

    def test_string(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(STRING_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(STRING_TEST))
        self.assertEqual(STRING_TEST, json_decoded, xml_decoded)

    def test_none(self):
        json_decoded = json_serializer.loads(json_serializer.dumps(NONE_TEST))
        xml_decoded = xml_serializer.loads(xml_serializer.dumps(NONE_TEST))
        self.assertEqual(NONE_TEST, json_decoded, xml_decoded)



if __name__ == '__main__':
    unittest.main()
