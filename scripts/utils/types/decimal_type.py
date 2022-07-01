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
        minInclusive = node_type.get("minInclusive", None)
        maxInclusive = node_type.get("maxInclusive", None)
        value = None
        if minInclusive is not None and maxInclusive is not None:
            value = Fake_.random_int(min=node_type['minInclusive'], max=node_type['maxInclusive'])
        totalDigits = node_type.get("totalDigits", None)
        if totalDigits is not None:
            pattern = "#" * totalDigits
            value = str(value)[:totalDigits] if value is not None else Fake_.numerify(text=pattern)
        if value is  None:
            value = Fake_.numerify(text="###")
        return str(value)
