import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_

'''

'''


class StringType():
    name: str = "string"

    def value(self, node_type):
        all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
        value = None
        type_ = dict()
        for attr in all_facets_types:
            type_[attr] = get_value_from_facet(node_type.facets, attr)
        if all(element in all_facets_types for element in ['enumeration']):
            index = Fake_.random_int(min=0, max=len(type_['enumeration'])-1)
            if 'length' in type_.keys():
                value=type_['enumeration'][index][:type_['length']]
            else:
                value=type_['enumeration'][index]

        return value
