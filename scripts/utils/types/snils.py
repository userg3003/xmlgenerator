import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class SnilsType():
    name: str = "СНИЛСТип"

    def value(self, node_type, sync_attr=None):
        logger.trace(f"{SnilsType.name} node_type: {node_type} param: {sync_attr}")
        value=None
        if node_type.get("patterns", None) is not None and node_type["patterns"][0] == '\\d{11}' :
            value = format(sync_attr, f"011d")
            # value = rstr.xeger(node_type['patterns'][0])

        else:
            div = " " if sync_attr % 2 else "-"
            value = format(sync_attr, f"011d")
            value = f"{value[:3]}-{value[3:6]}-{value[6:9]}{div}{value[9:11]}"
        logger.trace(f"{SnilsType.name} value: {value}  param: {sync_attr}")
        return value
