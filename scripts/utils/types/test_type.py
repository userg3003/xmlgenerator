import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class TESTType():
    name: str = "ТЕСТТип"

    def value(self, node_type, sync_attr=None):
        value = None
        if node_type['pattern'] is not None:
            value = rstr.xeger(node_type['pattern'][0])
        else:
            pattern = "#" * 2
            value = Fake_.numerify(text=pattern)
        return value
