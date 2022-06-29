import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class TESTType():
    name: str = "ТЕСТТип"

    def value(self, node_type):
        all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
        type_ = dict()
        for attr in all_facets_types:
            type_[attr] = get_value_from_facet(node_type.facets, attr)
        value = None
        if all(element in all_facets_types for element in ['pattern']):
            value = rstr.xeger(type_['pattern'])
        return value


