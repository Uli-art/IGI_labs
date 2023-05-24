import argparse, configparser
from ObjectSerializer.SerializerFactory import SerializerFactory

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", help="file to deserialize object from", type=str)
    parser.add_argument("--file_from", help="file to deserialize object from", type=str)
    parser.add_argument("--file_to", help="file to serialize object", type=str)
    parser.add_argument("--format_from", help="input file format", type=str)
    parser.add_argument("--format_to", help="output file format", type=str)

    args = parser.parse_args()
    serializer_factory = SerializerFactory()
    if args.conf:
        config = configparser.ConfigParser()
        config.read(args.conf)
        defaults = config['Defaults']

        from_serializer = serializer_factory.create_serializer(defaults['format_from'])
        to_serializer = serializer_factory.create_serializer(defaults['format_to'])

        from_file = open(defaults['file_from'], "r")
        obj = from_serializer.load(from_file)
        from_file.close()

        to_file = open(defaults['file_to'], "w")
        to_serializer.dump(obj, to_file)
        to_file.close()



    from_serializer = serializer_factory.create_serializer(args.format_from)
    to_serializer = serializer_factory.create_serializer(args.format_to)

    from_file = open(args.file_from, "r")
    obj = from_serializer.load(from_file)
    from_file.close()

    to_file = open(args.file_to, "w")
    to_serializer.dump(obj, to_file)
    to_file.close()


