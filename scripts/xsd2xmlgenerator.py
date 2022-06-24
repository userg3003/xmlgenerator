import random
from decimal import Decimal, getcontext
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
            #  logger.debug(f" start node")
            self.root = ElementTree.Element(xsd_node.local_name)
            print(f"-------------- {xsd_node.local_name} =============== {self.schema.filepath}")
            self._recur_func(xsd_node=xsd_node, xml_node=self.root, is_root=True)
            #  logger.debug(f" --------------- stop node")

    def _recur_func(self, xsd_node, xml_node, is_root=False, fake_value=None):
        #  logger.debug(f" ---------------             iter node")
        if not is_root:
            xml_node = ElementTree.SubElement(xml_node, xsd_node.local_name)

        #  logger.debug(f"xsd_node.name: {xsd_node.name}")
        # simple content
        if xsd_node.type.is_simple():
            #  logger.debug(f"")
            xml_node.text = self.get_value_for_attribute(xsd_node, xsd_node.type, fake_value)
        # complex types
        else:
            #  logger.debug(f"{xsd_node.name}  {xsd_node.type}  {xsd_node.type.content}")
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
        #  logger.debug(f"")

        # attributes
        for attr, attr_obj in xsd_node.attributes.items():
            #  logger.debug(f"attr: {attr}")
            xml_node.attrib[attr] = self.get_value_for_attribute(attr_obj, attr_obj.type)
            #  logger.debug(f"xml_node.attrib[attr]: {xml_node.attrib[attr]}")
        #  logger.debug(f"")

    def write(self, xml_path) -> None:
        if self.root is None:
            # logger.error(f"Пустой root.")
            return
        tree = ElementTree.ElementTree(self.root)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
        print("Сгенерирован " + xml_path + " \nOk!!!")

    def validate(self, xml_path):
        self.schema.validate(xml_path)
        print(xml_path + " validates = " + str(self.schema.is_valid(xml_path)))

    def get_value_for_attribute(self, node, node_type, fake_value=None):
        #  logger.debug(f"node.name: {node.name}")
        self.all_types.add(node_type.local_name)
        self.all_attr.add(f"{node.name} \t:\t {node_type}")
        #  logger.debug(f"")
        if fake_value is None:
            #  logger.debug(f"")
            value = self.fake_attribute(node)
        else:
            #  logger.debug(f"")
            value = str(fake_value)
        #  logger.debug(f"")
        return value

    def get_pr_otsutsv(self, group):
        for i, item in enumerate(group):
            if "ПрОтс" in item.name:
                return i, item
        return -1, None

    def fake_attribute(self, node):
        #  logger.debug(f"node: {node.name}  {node} ")
        node_name = node.name
        value = None
        if node_name == "КолДок":
            is_count = random.choice([True, False])
            if is_count:
                value = str(self.count)
            else:
                value = self._faker.value(node_name)
            return value
        #  logger.debug(f"node: {node.name}  {node} ")
        value = self._faker.value(node_name)
        #  logger.debug(f"node: {node.name}  {node} value: {value}")
        if value is not None:
            return value
        pattern = node.type.facets.get("{http://www.w3.org/2001/XMLSchema}pattern", False)
        #  logger.debug(f"node: {node.name}  {node} ")
        if pattern:
            #  logger.debug(f"node: {node.name}  {node} ")
            value = ''
            for pattern in pattern.regexps:
                value = rstr.xeger(pattern)
                if value != "":
                    return value

            if node.name == "ДатаРожд":
                self.cur_birthday = value
        else:
            #  logger.debug(f"node: {node.name}  {node} ")
            if node.name == "ГодРожд":
                value = self.cur_birthday[-4:] if self.cur_birthday is not None else f"{self.fake.year()}"
            elif node.name == "МесГодРожд":
                value = self.cur_birthday[
                        -7:] if self.cur_birthday is not None else f"{self.fake.month()}.{self.fake.year()}"
        #  logger.debug(f"node: {node.name}  {node} ")
        if value is None:
            #  logger.debug(f"node: {node.name}  {node} ")
            if node.type.enumeration is not None:
                #  logger.debug(f"node: {node.name}  {node} ")
                value = self.fake.random_element(elements=node.type.enumeration)
                #  logger.debug(f"node: {node.name}  {node} ")
                return value
            #  logger.debug(f"node: {node.name}  {node} ")
            all_types = self.parse_type(node.type, node.name)
            #  logger.debug(f"node: {node.name}  {node} ")
            if isinstance(all_types, list):
                #  logger.debug(f"node: {node.name}  {node} ")
                value = self.generate_value(all_types, node.name)
                #  logger.debug(f"node: {node.name}  {node} ")
                return value

            type_name = all_types
            if type_name == "boolean":
                value = random.choice(["true", "false"])
            else:
                value = "????"
        #  logger.debug(f"node: {node.name}  {node} value: {value}")
        return value

    def generate_value(self, types, node_name):
        #  logger.debug(f"node_name: {node_name}  types: {types}")
        if node_name in self._faker.all_faker.keys():
            value = self._faker[node_name].value
            return value
        value = ""
        index = 0
        if len(types) > 2:
            index = random.randint(0, len(types) - 1)
        elif len(types) == 2:
            index = 1

        if types[index]['type_name'] == "string":
            if 'max_length' in types[index].keys() and types[index]['max_length'] == 0:
                return ""
            length = types[index]['max_length'] - 1 - len(node_name) if 'max_length' in types[index].keys() else 50
            if length < 0:
                length = types[index]['max_length']
            if length >= 10:
                length = random.randint(10, length)
                text = self.fake.text(max_nb_chars=length)
            else:
                text = self.fake.word()[:length]
            value = f"{node_name} {text}"[:length]
        elif types[index]['type_name'] == "decimal":
            #  logger.debug(f"types[index]: {types[index]}")
            fraction_digits = 0
            total_digits = 0
            if "totalDigits" in types[index].keys():
                total_digits = types[index]['totalDigits']
            if "fractionDigits" in types[index].keys() and types[index]['fractionDigits'] is not None:
                all_digits = abs(total_digits - types[index]['fractionDigits'])
                fraction_digits = str(
                    self.fake.random_number(digits=types[index]['fractionDigits'], fix_len=False))
            else:
                all_digits = total_digits
            value = str(self.fake.random_number(digits=all_digits, fix_len=True))
            value = value[0:random.randint(1, all_digits)]
            if "fractionDigits" in types[index].keys() is not None:
                value = f"{value}.{fraction_digits}"
        elif types[index]['type_name'] == "boolean":
            #  logger.debug(f"boolean types[index] {types[index]}")
            value = random.choice(["true", "false"])
        elif types[index]['type_name'] == "double":
            value = str(random.randint(types[index]['minInclusive'], types[index]['maxInclusive']))
            #  logger.debug(f"double types[index] {types[index]} value: {value}")
        elif types[index]['type_name'] == "integer" or types[index]['type_name'] == "int":
            max_value = None
            min_value = 0
            if "totalDigits" in types[index].keys():
                value = str(self.fake.random_number(digits=types[index]['totalDigits'], fix_len=True))
            else:
                if "max_value" in types[index].keys():
                    max_value = types[index]['max_value']
                if "min_value" in types[index].keys():
                    min_value = types[index]['min_value']
                if max_value is None:
                    value = self.fake.random_int(min=min_value)
                else:
                    value = self.fake.random_int(min=min_value, max=max_value)
            return str(value)
            #  logger.debug(f"double types[index] {types[index]} value: {value}")
        elif types[index]['type_name'] == "short":
            max_value = None
            min_value = 0
            if "totalDigits" in types[index].keys():
                value = str(self.fake.random_number(digits=types[index]['totalDigits'], fix_len=True))
            else:
                if "max_value" in types[index].keys():
                    max_value = types[index]['max_value']
                if "min_value" in types[index].keys():
                    min_value = types[index]['min_value']
                if max_value is None:
                    value = self.fake.random_int(min=min_value)
                else:
                    value = self.fake.random_int(min=min_value, max=max_value)
            return str(value)
        else:
            value = ""
            if "patterns" in types[index].keys() and types[index]['patterns']:
                # regexps = types[index]['patterns'].regexps[0]
                regexps = types[index]['patterns'].patterns[0].pattern
                while value == '':
                    value = rstr.xeger(regexps)
                value = str(value)
            else:
                logger.warning(f"type not defined {types[index]['type_name']}")
                value = f"{node_name} {types[index]['type_name']}"

        return value

    @staticmethod
    def parse_type(node_type, node_name):
        #  logger.debug(f"node: {node_name}  {node_type} ")
        if isinstance(node_type, XsdUnion):
            #  logger.debug(f"node: {node_name}  {node_type} ")
            node_types = list()
            for member_type in node_type.member_types:
                type_ = {
                    "type_name": member_type.root_type.local_name,
                    "max_length": member_type.max_length,
                    "min_length": member_type.min_length,
                    "max_value": member_type.max_value,
                    "min_value": member_type.min_value,
                    "patterns": member_type.patterns
                }
                all_facets_types = [item.split("}")[1] for item in member_type.facets if item is not None]
                #  logger.debug(f"all_facets_types: {all_facets_types}")
                for attr in all_facets_types:
                    type_[attr] = Xsd2XmlGenerator.get_value_from_facet(member_type.facets, attr)

                if member_type.patterns is not None:
                    logger.warning(f"patterns: {member_type.patterns}")
                node_types.append(type_)
            #  logger.debug(f"node: {node_name}  {node_type} ")
            return node_types

        local_type_name = getattr(node_type, "local_name")
        #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
        if local_type_name is not None:
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            type_ = {"type_name": local_type_name,
                     "max_length": node_type.max_length,
                     "min_length": node_type.min_length,
                     "max_value": node_type.max_value,
                     "min_value": node_type.min_value,
                     "patterns": node_type.patterns, }
            # type_ = {"type_name": local_type_name}
            # type_["max_length"] = node_type.max_length
            # type_["min_length"] = node_type.min_length
            # type_["max_value"] = node_type.max_value
            # type_["min_value"] = node_type.min_value
            # type_["patterns"] = node_type.patterns
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            for attr in all_facets_types:
                #  logger.debug(f"node: {node_name}  {node_type}  attr: {attr}")
                type_[attr] = Xsd2XmlGenerator.get_value_from_facet(node_type.facets, attr)
                #  logger.debug(f"node: {node_name}  {node_type}  type_[attr]: {type_[attr]}")
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            return type_
        local_type_name = getattr(node_type.base_type, "local_name")
        #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
        if local_type_name == "string":
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
            type_ = {"type_name": "string"}
            for attr in all_facets_types:
                type_[attr] = Xsd2XmlGenerator.get_value_from_facet(node_type.facets, attr)
            Xsd2XmlGenerator.set_max_min(node_type, type_)
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            return [type_]
        if local_type_name == "double":
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
            type_ = {"type_name": "double"}
            for attr in all_facets_types:
                type_[attr] = Xsd2XmlGenerator.get_value_from_facet(node_type.facets, attr)
            type_["max_length"] = node_type.max_length
            type_["min_length"] = node_type.min_length
            type_["max_value"] = node_type.max_value
            type_["min_value"] = node_type.min_value
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            return [type_]
        #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
        if local_type_name == "integer":
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
            type_ = {"type_name": "integer"}
            for attr in all_facets_types:
                type_[attr] = Xsd2XmlGenerator.get_value_from_facet(node_type.facets, attr)
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            Xsd2XmlGenerator.set_max_min(node_type, type_)
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            return [type_]
        #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
        if local_type_name == "decimal":
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
            type_ = {"type_name": "decimal"}
            for attr in all_facets_types:
                type_[attr] = Xsd2XmlGenerator.get_value_from_facet(node_type.facets, attr)
                type_[attr] = float(type_[attr]) if isinstance(type_[attr], Decimal) else type_[attr]
            if node_type.max_length is not None:
                type_["max_length"] = node_type.max_length
            if node_type.min_length is not None:
                type_["min_length"] = node_type.min_length
            if node_type.max_value is not None:
                type_["max_value"] = float(node_type.max_value)
            if node_type.max_length is not None:
                type_["min_value"] = float(node_type.min_value)
            if node_type.patterns is not None:
                type_["patterns"] = node_type.patterns
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            return [type_]
        #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
        if local_type_name is None:
            #  logger.debug(f"local_type_name from node.base_type: {local_type_name}")
            return local_type_name
        #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
        if local_type_name is not None:
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
            type_ = {"type_name": local_type_name}
            for attr in all_facets_types:
                type_[attr] = Xsd2XmlGenerator.get_value_from_facet(node_type.facets, attr)
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            Xsd2XmlGenerator.set_max_min(node_type, type_)
            #  logger.debug(f"node: {node_name}  {node_type}  local_type_name: {local_type_name}")
            return [type_]
        #  logger.debug(f"NodeType not defined")
        return None

    @staticmethod
    def set_max_min(node_type, type_):
        if node_type.max_length is not None:
            type_["max_length"] = node_type.max_length
        if node_type.min_length is not None:
            type_["min_length"] = node_type.min_length
        if node_type.max_value is not None:
            type_["max_value"] = node_type.max_value
        if node_type.min_value is not None:
            type_["min_value"] = node_type.min_value
        if node_type.patterns is not None:
            type_["patterns"] = node_type.patterns

    @staticmethod
    def get_value_from_facet(facet, name_value):
        name_key = f'{{http://www.w3.org/2001/XMLSchema}}{name_value}'
        value = None
        if name_value == "pattern":
            value = getattr(facet[name_key], "patterns", None) if facet.get(name_key, None) else None
            value = value[0].pattern if value is not None else None
        else:
            value = getattr(facet[name_key], "value", None)
        return value
