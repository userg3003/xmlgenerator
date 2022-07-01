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
    all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
    type_ = dict()
    for attr in all_facets_types:
        type_[attr] = get_value_from_facet(node_type.facets, attr)
    length = type_['length'] if 'length' in type_.keys() else None
    length = type_['maxLength'] if 'maxLength' in type_.keys() else length
    # pattern = type_['pattern'] if 'pattern' in type_.keys() else None
    logger.trace(f"{node_type}  type_: {type_}")
    pref = "01"

    value = None
    if all(element in all_facets_types for element in ['pattern']):
        value = rstr.xeger(type_['pattern'])
    logger.trace(f"{node_type}  length: {length} value: {value}")
    if length is None:
        logger.trace(f"{node_type}  param: {param}")
        if getattr(node_type, "member_types", None) is not None:
            type_ = get_for_member(node_type.member_types)
            logger.trace(f"{node_type}  param: {param}")
            length = type_['length'] if 'length' in type_.keys() else None
            length = type_['maxLength'] if 'maxLength' in type_.keys() else length
            logger.trace(f"{node_type}  param: {param}")
        elif getattr(node_type, "base_type", None) is not None:
            logger.trace(f"{node_type}  param: {param}")
            all_facets_types = [item.split("}")[1] for item in node_type.base_type.facets if item is not None]
            for attr in all_facets_types:
                type_[attr] = get_value_from_base_type_facet(node_type, attr)
            length = type_['length'] if 'length' in type_.keys() else None
            length = type_['maxLength'] if 'maxLength' in type_.keys() else length
            if length is None:
                if  is_fl is not None:
                    if is_fl:
                        length = 12
                    else:
                        length = 10
                else:
                    length =12

            logger.trace(f"{node_type}  type_: {type_}")
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
