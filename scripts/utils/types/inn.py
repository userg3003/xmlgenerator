import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class InnYLType():
    name: str = "ИННЮЛТип"

    def value(self, node_type):
        value = get_inn(node_type)
        return value


class InnFLType():
    name: str = "ИННФЛТип"

    def value(self, node_type):
        value = get_inn(node_type)
        return value

def get_inn(node_type):
    all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
    type_ = dict()
    for attr in all_facets_types:
        type_[attr] = get_value_from_facet(node_type.facets, attr)
    length = type_['length'] if 'length' in type_.keys() else 10
    length = type_['maxLength'] if 'maxLength' in type_.keys() else length
    pattern = "#" * length
    value = Fake_.numerify(text=pattern)
    return value
