import random
from loguru import logger
from xml.etree import ElementTree
from faker import Faker
from faker.providers import date_time, internet, lorem, person, python

import xmlschema
import rstr

from scripts.utils.fakers import Fakers

random.seed()

Faker.seed(random.randint(1, 100))


def make_fake():
    fake = Faker("ru_RU")
    fake.add_provider(person)
    fake.add_provider(internet)
    fake.add_provider(python)
    fake.add_provider(date_time)
    return fake


def get_random_value():
    return int(random.randrange(2, 10))


class Xsd2XmlGenerator:

    def __init__(self, xsd_path, count):
        self.schema = xmlschema.XMLSchema(xsd_path)
        self.root = None
        self.cur_birthday = None
        self.cur_fio = None
        self.all_types = set()
        self.all_attr = set()
        self.fake = make_fake()
        self.count = count
        self._faker = Fakers()

    def generate(self):
        # идем по всем рутовым элементам
        for xsd_node in self.schema.root_elements:
            self.root = ElementTree.Element(xsd_node.local_name)
            # print(f"-------------- {xsd_node.local_name} =============== ")
            self._recur_func(xsd_node=xsd_node, xml_node=self.root, is_root=True)

    def _recur_func(self, xsd_node, xml_node, is_root=False):
        if not is_root:
            xml_node = ElementTree.SubElement(xml_node, xsd_node.local_name)

        # simple content
        if xsd_node.type.is_simple():
            xml_node.text = self.get_value_for_attribute(xsd_node, xsd_node.type)
        # complex types
        else:
            group = xsd_node.type.content._group
            for sub_node in group:
                if sub_node.occurs[1] is None:
                    if sub_node.parent.parent.parent.parent is None:
                        i = self.count
                    else:
                        i = get_random_value()
                else:
                    i = 1
                while i != 0:
                    i -= 1
                    if hasattr(sub_node, '_group'):
                        for item_node in sub_node._group:
                            self._recur_func(item_node, xml_node)
                        continue
                    self._recur_func(sub_node, xml_node)

        # attributes
        for attr, attr_obj in xsd_node.attributes.items():
            xml_node.attrib[attr] = self.get_value_for_attribute(attr_obj, attr_obj.type)

    def write(self, xml_path) -> None:
        tree = ElementTree.ElementTree(self.root)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
        print("Generate " + xml_path + " \nDone!!!")

    def validate(self, xml_path):
        self.schema.validate(xml_path)
        print(xml_path + " validates = " + str(self.schema.is_valid(xml_path)))

    def get_value_for_attribute(self, node, node_type):
        self.all_types.add(node_type.local_name)
        self.all_attr.add(f"{node.name} \t:\t {node_type}")
        value = self.fake_attribute(node)
        return value

    def fake_attribute(self, node):
        node_name = node.name
        value = None
        if node_name == "КолДок":
            is_count = random.choice([True, False])
            if is_count:
                value = str(self.count)
            else:
                value = self._faker.value(node_name)
            return value
        value = self._faker.value(node_name)
        if value is not None:
            return value
        pattern = node.type.facets.get("{http://www.w3.org/2001/XMLSchema}pattern", False)
        if pattern:
            regexps = pattern.regexps[0]
            value = ''
            while value == '':
                value = rstr.xeger(regexps)
            if node.name == "ДатаРожд":
                self.cur_birthday = value
        else:
            if node.name == "ГодРожд":
                value = self.cur_birthday[-4:]
            elif node.name == "МесГодРожд":
                value = self.cur_birthday[-7:]
        if value is None:
            local_type_name = node.type.local_name
            if node.type.enumeration is not None:
                value = self.fake.random_element(elements=node.type.enumeration)
                return value
            if local_type_name is None:
                local_type_name = node.type.base_type.local_name
            if local_type_name == "string":
                length = node.type.max_length - 1 - len(node.name)
                if length < 0:
                    length = node.type.max_length
                if length >= 10:
                    length = random.randint(10, length)
                    text = self.fake.text(max_nb_chars=length)
                else:
                    text = self.fake.word()[:length]
                value = f"{node.name} {text}"[:length]


            else:
                value = "????"
        return value
