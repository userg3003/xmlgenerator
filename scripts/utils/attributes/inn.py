from loguru import logger
from scripts.utils.attributes.attributes import Faker_
from scripts.utils.types.inn import get_inn


class InnFL(Faker_):
    name: str = "ИННФЛ"

    @property
    def value(self):
        value = Faker_._fake.last_name()
        value = get_inn(None)
        logger.debug(f"{InnFL.name} value: {value}")
        return value


class InnYL(Faker_):
    name: str = "ИННЮЛ"

    @property
    def value(self):
        value = Faker_._fake.last_name()
        value = get_inn(None)
        logger.debug(f"{InnYL.name} value: {value}")
        return value


class Inn(Faker_):
    name: str = "ИНН"

    @property
    def value(self):
        value = Faker_._fake.last_name()
        value = get_inn(None)
        logger.debug(f"{Inn.name} value: {value}")
        return value
