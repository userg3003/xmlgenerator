import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class InnYLType():
    name: str = "ИННЮЛТип"

    def value(self, node_type, sync_attr=None):
        # value = get_inn(node_type, sync_attr)
        value = get_inn_fl(sync_attr)
        logger.trace(f"{InnYLType.name} value: {value} param: {sync_attr}")
        return value


class InnFLType():
    name: str = "ИННФЛТип"

    def value(self, node_type, sync_attr=None):
        # value = get_inn(node_type, sync_attr)
        value = get_inn_fl(sync_attr)
        logger.trace(f"{InnYLType.name} value: {value} param: {sync_attr}")
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


def get_inn(node_type, param):
    logger.trace(f"{node_type}  param: {param}")
    if node_type is None:
        return "ИНН ТИП None"
    all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
    type_ = dict()
    for attr in all_facets_types:
        type_[attr] = get_value_from_facet(node_type.facets, attr)
    length = type_['length'] if 'length' in type_.keys() else None
    length = type_['maxLength'] if 'maxLength' in type_.keys() else length
    # pattern = type_['pattern'] if 'pattern' in type_.keys() else None
    pref = "01"

    value = None
    if all(element in all_facets_types for element in ['pattern']):
        value = rstr.xeger(type_['pattern'])
    if length is None:
        type_ = get_for_member(node_type.member_types)
        length = type_['length'] if 'length' in type_.keys() else None
        length = type_['maxLength'] if 'maxLength' in type_.keys() else length
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
