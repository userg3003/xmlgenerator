import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet, get_value_from_base_type_facet
from scripts.utils.types import Fake_


class InnYLType():
    name: str = "ИННЮЛТип"

    def value(self, node_type, sync_attr=None):
        logger.trace(f"{InnYLType.name} value: {node_type} param: {sync_attr}")
        value = get_inn(node_type, sync_attr, False)
        # value = get_inn_fl(sync_attr)
        logger.trace(f"{InnYLType.name} value: {value} param: {sync_attr}")
        return value


class InnFLType():
    name: str = "ИННФЛТип"

    def value(self, node_type, sync_attr=None):
        logger.trace(f"{InnFLType.name} value: {node_type} sync_attr: {sync_attr}")
        value = get_inn(node_type, sync_attr, True)
        # value = get_inn_fl(sync_attr)
        logger.trace(f"{InnYLType.name} value: {value} sync_attr: {sync_attr}")
        return value


def get_inn_fl(sync_attr):
    pref = "01"
    length = 12
    value = pref + format(sync_attr, f"0{length - 2}d")
    logger.trace(f"{InnFLType.name} value: {value} param: {sync_attr}")
    return value


def get_inn_yl(sync_attr):
    pref = "01"
    length = 10
    value = pref + format(sync_attr, f"0{length - 2}d")
    logger.trace(f"{InnYLType.name} value: {value} param: {sync_attr}")
    return value


def get_inn(node_type, param, is_fl=None):
    logger.trace(f"{node_type}  param: {param}")
    if node_type is None:
        return "ИНН ТИП None"
    length = node_type.get('max_length', None)# node_type['length'] if node_type['length'] is not None else None
    length = node_type.get('maxLength', length)
    # pattern = node_type['pattern'] if 'pattern' in type_.keys() else None
    pref = "01"

    value = None
    if node_type ['patterns'] is not None:
        value = rstr.xeger(node_type['patterns'][0])
    logger.trace(f"{node_type}  length: {length} value: {value}")
    if length is None:
        if  is_fl is not None:
            if is_fl:
                length = 12
            else:
                length = 10
        else:
            length =12

    logger.trace(f"{node_type}  param: {param}")
    value = pref + format(param, f"0{length - 2}d")
    return str(value)


def get_for_member(node_types):
    types = dict()
    for node_type in node_types:
        logger.trace(f"{node_type} ")
        if node_type is None:
            continue
        all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
        for attr in all_facets_types:
            types[attr] = get_value_from_facet(node_type.facets, attr)
    return types
