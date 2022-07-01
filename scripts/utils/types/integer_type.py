import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_

'''

'''


class IntType():
    name: str = "int"

    def value(self, node_type, sync_attr=None):
        value = get_value(node_type)
        return str(value)


def get_value(node_type):
    value = Fake_.random_int(min=node_type['minInclusive'], max=node_type['maxInclusive'])
    return value

def get_value_prev(node_type):
    all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
    type_ = dict()
    for attr in all_facets_types:
        type_[attr] = get_value_from_facet(node_type.facets, attr)
    value = Fake_.random_int(min=type_['minInclusive'], max=type_['maxInclusive'])
    return value


class IntegerType():
    name: str = "integer"

    def value(self, node_type, sync_attr=None):
        value = get_value(node_type)
        return None #str(value)


class LongType():
    name: str = "long"

    def value(self, node_type, sync_attr=None):
        value = get_value(node_type)
        return None #str(value)
