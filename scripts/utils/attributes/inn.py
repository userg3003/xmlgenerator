from loguru import logger
from scripts.utils.attributes.attributes import Faker_
from scripts.utils.types.inn import get_inn


class InnFL(Faker_):
    name: str = "ИННФЛ"

    def value(self, node_type=None, param=None):
        value = Faker_._fake.last_name()
        value = get_inn(node_type, param)
        logger.debug(f"{InnFL.name} value: {value} param: {param}")
        return value


class InnYL(Faker_):
    name: str = "ИННЮЛ"

    def value(self, node_type=None, param=None):
        value = Faker_._fake.last_name()
        value = get_inn(node_type, param)
        logger.debug(f"{InnYL.name} value: {value} param: {param}")
        return value


class Inn(Faker_):
    name: str = "ИНН"

    def value(self, node_type=None, param=None):
        value = Faker_._fake.last_name()
        value = get_inn(node_type, param)
        logger.debug(f"{Inn.name} value: {value} param: {param}")
        return value
