import random
from xml.etree import ElementTree
from faker import Faker
from faker.providers import date_time, internet, lorem, person, python

import xmlschema
import rstr


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

    def __init__(self, xsd_path):
        self.schema = xmlschema.XMLSchema(xsd_path)
        self.root = None
        self.cur_birthday = None
        self.cur_fio = None
        self.all_types = set()
        self.all_attr = set()
        self.fake = make_fake()

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
        value = self.fake_attribute(node.name)
        if value is not None:
            return value
        pattern = node_type.facets.get("{http://www.w3.org/2001/XMLSchema}pattern", False)
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
            else:
                value = str(random.randrange(100, 10000))
        return value

    def fake_attribute(self, node_name):
        if node_name == "Фамилия":
            value = self.fake.last_name()
            return value
        if node_name == "Отчество":
            value = self.fake.middle_name()
            return value
        if node_name == "Имя":
            value = self.fake.first_name()
            return value
        if node_name == "Город":
            value = self.fake.city_name()
            return value
        if node_name == "Тлф":
            value = self.fake.phone_number()
            return value
        if node_name == "Район":
            value = self.fake.city()
            return value
        if node_name == "Улица":
            value = self.fake.street_name()
            return value
        if node_name == "Дом":
            value = self.fake.building_number()
            return value
        if node_name == "Корпус":
            value = self.fake.building_number()
            return value
        if node_name == "Кварт":
            value = self.fake.building_number()
            return value
        if node_name == "ДолжОтв":
            value = self.fake.job()
            return value
        if node_name == "МестоРожд":
            value = f"{self.fake.administrative_unit()}, {self.fake.city()}"
            return value
        if node_name == "E-mail":
            value = self.fake.email()
            return value
        if node_name == "НаселПункт":
            value = self.fake.city()
            return value
        return None