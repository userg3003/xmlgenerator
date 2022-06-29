import random
import rstr
import string
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class SPDULType():
    name: str = 'СПДУЛТип'

    def value(self, node_type):
        all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
        all_facets_base_types = [item.split("}")[1] for item in node_type.base_type.facets if item is not None]
        base_type_ = dict()
        for attr in all_facets_base_types:
            base_type_[attr] = get_value_from_facet(node_type.base_type.facets, attr)
        type_ = dict()
        for attr in all_facets_types:
            type_[attr] = get_value_from_facet(node_type.facets, attr)
        length_base = base_type_['length'] if 'length' in base_type_.keys() else None
        length = type_['length'] if 'length' in type_.keys() else None
        # length = type_['maxLength'] if 'maxLength' in type_.keys() else length
        value = None
        if all(element in all_facets_base_types for element in ['enumeration']):
            index = Fake_.random_int(min=0, max=len(base_type_['enumeration']) - 1)
            if length_base is not None:
                value = base_type_['enumeration'][index][:base_type_['length']]
            else:
                value = base_type_['enumeration'][index]
        if all(element in all_facets_types for element in ['enumeration']):
            index = Fake_.random_int(min=0, max=len(type_['enumeration']) - 1)
            if length is not None:
                value = type_['enumeration'][index][:type_['length']]
            else:
                value = type_['enumeration'][index]
        if all(element in all_facets_base_types for element in ['pattern']) and not all(element in all_facets_types for element in ['enumeration']):
            value = rstr.xeger(base_type_['pattern'])
        if value is None and 'length' in base_type_.keys():
            value = ''.join(random.choices(string.ascii_letters, k=base_type_['length']))
        if value is None:
            pattern = "#" * 2
            value = Fake_.numerify(text=pattern)
        return value

class SPDULschType():
    name: str = 'СПДУЛШТип'

    def value(self, node_type):
        all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
        type_ = dict()
        for attr in all_facets_types:
            type_[attr] = get_value_from_facet(node_type.facets, attr)
        length = type_['length'] if 'length' in type_.keys() else None
        if length is None:
            length = type_['maxLength'] if 'maxLength' in type_.keys() else None
        # length = type_['maxLength'] if 'maxLength' in type_.keys() else length
        value = None
        if all(element in all_facets_types for element in ['enumeration']):
            index = Fake_.random_int(min=0, max=len(type_['enumeration']) - 1)
            if length is not None:
                value = type_['enumeration'][index][:type_['length']]
            else:
                value = type_['enumeration'][index]
        if all(element in all_facets_types for element in ['pattern']):
            value = rstr.xeger(type_['pattern'])
        if value is None and 'length' in type_.keys():
            value = ''.join(random.choices(string.ascii_letters, k=type_['length']))
        if value is None:
            pattern = "#" * 2
            value = Fake_.numerify(text=pattern)
        return value

