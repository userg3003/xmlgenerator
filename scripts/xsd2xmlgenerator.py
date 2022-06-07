import random
from loguru import logger
from xml.etree import ElementTree
from faker import Faker
from faker.providers import date_time, internet, lorem, person, python

import xmlschema
from xmlschema.validators import XsdUnion
import rstr

from scripts.utils.fakers import Fakers

random.seed()

Faker.seed(random.randint(1, 1000))


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

    def _recur_func(self, xsd_node, xml_node, is_root=False, fake_value=None):
        if not is_root:
            xml_node = ElementTree.SubElement(xml_node, xsd_node.local_name)

        # simple content
        if xsd_node.type.is_simple():
            xml_node.text = self.get_value_for_attribute(xsd_node, xsd_node.type, fake_value)
        # complex types
        else:
            # logger.debug(f"{xsd_node.type}  {xsd_node.type.content}")
            group = getattr(xsd_node.type.content, "_group", [])
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
                    model = getattr(sub_node, "model", None);
                    if hasattr(sub_node, '_group'):
                        fake_value = None
                        selected_item = -1
                        if model == 'choice':
                            selected_item = -1
                            index_pr_ots, item = self.get_pr_otsutsv(sub_node._group)
                            if item is not None:
                                selected_item = random.randint(0, len(sub_node._group) - 1)
                                if index_pr_ots == selected_item:
                                    fake_value = 1

                        for ind, item_node in enumerate(sub_node._group):
                            if ind == selected_item:
                                self._recur_func(item_node, xml_node, is_root, fake_value)
                        continue
                    self._recur_func(sub_node, xml_node, False)

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

    def get_value_for_attribute(self, node, node_type, fake_value=None):
        self.all_types.add(node_type.local_name)
        self.all_attr.add(f"{node.name} \t:\t {node_type}")
        if fake_value is None:
            value = self.fake_attribute(node)
        else:
            value = str(fake_value)
        return value

    def get_pr_otsutsv(self, group):
        for i, item in enumerate(group):
            if "ПрОтс" in item.name:
                return i, item
        return -1, None

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
            # logger.debug(f"{node.type}")
            if node.type.enumeration is not None:
                value = self.fake.random_element(elements=node.type.enumeration)
                return value
            all_types = self.parse_type(node.type)
            if isinstance(all_types, list):
                value = self.generate_value(all_types, node.name)
                return value

            type_name = all_types
            if type_name == "boolean":
                value = random.choice(["true", "false"])
            else:
                value = "????"
        return value

    def generate_value(self, types, node_name):
        value = ""
        index = random.randint(0, len(types) - 1)

        if types[index]['type_name'] == "string":
            if types[index]['max_length'] == 0:
                return ""
            length = types[index]['max_length'] - 1 - len(node_name)
            if length < 0:
                length = types[index]['max_length']
            if length >= 10:
                length = random.randint(10, length)
                text = self.fake.text(max_nb_chars=length)
            else:
                text = self.fake.word()[:length]
            value = f"{node_name} {text}"[:length]
        elif types[index]['type_name'] == "decimal":
            fractionDigits = 0
            if types[index]['fractionDigits'] is not None:
                all_digits = types[index]['totalDigits'] - types[index]['fractionDigits']
                fractionDigits = str(
                    self.fake.random_number(digits=types[index]['fractionDigits'], fix_len=False))
            else:
                all_digits = types[index]['totalDigits']
            value = str(self.fake.random_number(digits=all_digits, fix_len=True))
            value = value[0:random.randint(1, all_digits)]
            if types[index]['fractionDigits'] is not None:
                value = f"{value}.{fractionDigits}"
        elif types[index]['type_name'] == "boolean":
            logger.debug(f"boolean types[index] {types[index]}")
            value = random.choice(["true", "false"])

        return value

    @staticmethod
    def parse_type(node_type):
        if isinstance(node_type, XsdUnion):
            node_types = list()
            for member_type in node_type.member_types:
                type_ = {
                    "type_name": member_type.root_type.local_name,
                    "max_length": member_type.max_length,
                    "min_length": member_type.min_length,
                    "max_value": member_type.max_value,
                    "min_value": member_type.min_value,
                    "totalDigits": Xsd2XmlGenerator.getValueFromFacet(member_type.facets, "totalDigits"),
                    "fractionDigits": Xsd2XmlGenerator.getValueFromFacet(member_type.facets, "fractionDigits"),
                    "length": Xsd2XmlGenerator.getValueFromFacet(member_type.facets, "length"),
                    "maxLength": Xsd2XmlGenerator.getValueFromFacet(member_type.facets, "maxLength"),
                    "patterns": member_type.patterns
                }
                if member_type.patterns is not None:
                    logger.debug(f"patterns: {member_type.patterns}")
                node_types.append(type_)
            return node_types

        local_type_name = getattr(node_type, "local_name")
        if local_type_name is not None:
            logger.debug(f"local_type_name from node.type: {local_type_name}")
            return local_type_name
        local_type_name = getattr(node_type.base_type, "local_name")
        if local_type_name is None:
            logger.debug(f"local_type_name from node.base_type: {local_type_name}")
            return local_type_name
        logger.debug(f"NodeType not defined")
        return None

    @staticmethod
    def getValueFromFacet(facet, nameValue):
        nameKey = f'{{http://www.w3.org/2001/XMLSchema}}{nameValue}'
        value = facet[nameKey].value if facet.get(nameKey, None) else None
        return value
