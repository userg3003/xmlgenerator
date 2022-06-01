import uuid

from xsd2xmlgenerator import Xsd2XmlGenerator

xml_name = str(uuid.uuid4())


def main():
    # generator = Xsd2XmlGenerator(xsd_path="resources/xsd-test.xsd")
    generator = Xsd2XmlGenerator(xsd_path="tests/data/root.xsd")
    generator.generate()
    generator.write(xml_path="tests/data/" + xml_name + ".xml")
    # generator.validate(xml_path="tests/data/" + xml_name + ".xml")



if __name__ == "__main__":
    main()
