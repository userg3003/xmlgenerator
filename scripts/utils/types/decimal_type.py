import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_

'''

'''


class DecimalType():
    name: str = "decimal"

    def value(self, node_type, sync_attr=None):
        all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
        type_ = dict()
        value=None
        for attr in all_facets_types:
            type_[attr] = get_value_from_facet(node_type.facets, attr)
        if all(element in all_facets_types for element in ['minInclusive', 'maxInclusive']):
            value = Fake_.random_int(min=type_['minInclusive'], max=type_['maxInclusive'])
        if "totalDigits" in all_facets_types:
            pattern = "#" * type_["totalDigits"]
            value = str(value)[:type_["totalDigits"]] if value is not None else Fake_.numerify(text=pattern)
        return value
