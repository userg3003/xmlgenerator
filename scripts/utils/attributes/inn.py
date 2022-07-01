from loguru import logger
from scripts.utils.attributes.attributes import Faker_
from scripts.utils.types.inn import get_inn, get_inn_fl, get_inn_yl


class InnFL(Faker_):
    name: str = "ИННФЛ"

    def value(self, node_type=None, param=None):
        logger.trace(f"{Inn.name} value: {node_type} param: {param}")
        value = get_inn(node_type, param, is_fl=True)
        # value = get_inn_fl(param)
        logger.trace(f"{InnFL.name} value: {value} param: {param}")
        return value


class InnYL(Faker_):
    name: str = "ИННЮЛ"

    def value(self, node_type=None, param=None):
        logger.trace(f"{Inn.name} value: {node_type} param: {param}")
        value = get_inn(node_type, param, is_fl=False)
        # value = get_inn_yl(param)
        logger.trace(f"{InnYL.name} value: {value} param: {param}")
        return value


class Inn(Faker_):
    name: str = "ИНН"

    def value(self, node_type=None, param=None):
        logger.trace(f"{Inn.name} value: {node_type} param: {param}")
        value = get_inn(node_type, param)
        logger.trace(f"{Inn.name} value: {value} param: {param}")
        return value
