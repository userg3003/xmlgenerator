from loguru import logger
from datetime import date
import random
import scripts.utils as util
from scripts.utils.types.number_abonent import NumberAbonentType
from scripts.utils.types.integer_type import IntegerType, LongType, IntType
from scripts.utils.types.decimal_type import DecimalType
from scripts.utils.types.snils import SnilsType
from scripts.utils.types.string_type import StringType
from scripts.utils.types.data_type import DataType
from scripts.utils.types.inn import InnFLType, InnYLType


class Faker_:
    _fake = util.make_fake()

    def __init__(self):
        self._name = None
        self._value = None

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


class LastName(Faker_):
    name: str = "Фамилия"

    @property
    def value(self):
        return Faker_._fake.last_name()


class FirstName(Faker_):
    name: str = "Имя"

    @property
    def value(self):
        return Faker_._fake.first_name()


class MiddleName(Faker_):
    name: str = "Отчество"

    @property
    def value(self):
        return Faker_._fake.middle_name()


class CityName(Faker_):
    name: str = "Город"

    @property
    def value(self):
        return Faker_._fake.city_name()


class PhoneNumber(Faker_):
    name: str = "Тлф"

    @property
    def value(self):
        return Faker_._fake.phone_number()


class Region(Faker_):
    name: str = "Район"

    @property
    def value(self):
        return Faker_._fake.city()


#
class StreetName(Faker_):
    name: str = "Улица"

    @property
    def value(self):
        return Faker_._fake.street_name()


#
class BuildingNumber(Faker_):
    name: str = "Дом"

    @property
    def value(self):
        return Faker_._fake.building_number()


#
class BuildingHouse(Faker_):
    name: str = "Корпус"

    @property
    def value(self):
        return Faker_._fake.building_number()


#
class Quarter(Faker_):
    name: str = "Кварт"

    @property
    def value(self):
        return Faker_._fake.building_number()


#
class Job(Faker_):
    name: str = "ДолжОтв"

    @property
    def value(self):
        return Faker_._fake.job()


class Email(Faker_):
    name: str = "E-mail"

    @property
    def value(self):
        return Faker_._fake.email()


class Locality(Faker_):
    name: str = "НаселПункт"

    @property
    def value(self):
        return Faker_._fake.city()


class BirthPlace(Faker_):
    name: str = "МестоРожд"

    @property
    def value(self):
        return f"{Faker_._fake.administrative_unit()}, {Faker_._fake.city()}"


class Year(Faker_):
    name: str = "Год"

    @property
    def value(self):
        return Faker_._fake.year()


class Month(Faker_):
    name: str = "Месяц"

    @property
    def value(self):
        return Faker_._fake.month()


class Day(Faker_):
    name: str = "День"

    @property
    def value(self):
        return Faker_._fake.day_of_month()


class KolDok(Faker_):
    name: str = "КолДок"

    @property
    def value(self):
        return str(random.randrange(1, 1000))


class Fakers:
    def __init__(self):
        self.all_faker = dict()
        self.all_faker[LastName.name] = LastName()
        self.all_faker[FirstName.name] = FirstName()
        self.all_faker[MiddleName.name] = MiddleName()
        self.all_faker[CityName.name] = CityName()
        self.all_faker[PhoneNumber.name] = PhoneNumber()
        self.all_faker[Region.name] = Region()
        self.all_faker[StreetName.name] = StreetName()
        self.all_faker[BuildingNumber.name] = BuildingNumber()
        self.all_faker[BuildingHouse.name] = BuildingHouse()
        self.all_faker[Quarter.name] = Quarter()
        self.all_faker[Job.name] = Job()
        self.all_faker[Email.name] = Email()
        self.all_faker[Locality.name] = Locality()
        self.all_faker[BirthPlace.name] = BirthPlace()
        self.all_faker[KolDok.name] = Email()
        self.all_faker[Month.name] = Month()
        self.all_faker[Day.name] = Day()
        self.all_faker[Year.name] = Year()
        self.all_types = dict()
        self.all_types[NumberAbonentType.name] = NumberAbonentType()
        self.all_types[IntegerType.name] = IntegerType()
        self.all_types[LongType.name] = LongType()
        self.all_types[IntType.name] = IntType()
        self.all_types[DecimalType.name] = DecimalType()
        self.all_types[StringType.name] = StringType()
        self.all_types[SnilsType.name] = SnilsType()
        self.all_types[DataType.name] = DataType()
        self.all_types[InnFLType.name] = InnFLType()
        self.all_types[InnYLType.name] = InnYLType()

    def value(self, name, node_type=None):
        logger.trace(
            f"name: {name}   node_type: {node_type} node_type.local_name {node_type.local_name if node_type is not None else None}")
        if name in self.all_faker.keys():
            logger.trace(f"name: {name}   node_type: {node_type}")
            return self.all_faker[name].value
        elif node_type.local_name in self.all_types:
            logger.trace(f"name: {name}   node_type: {node_type}")
            return self.all_types[node_type.local_name].value(node_type)
        elif 'Дата' in name and node_type.local_name == "string":
            logger.trace(f"name: {name}   node_type: {node_type}")
            return self.date_value("%d.%m.%Y")
        elif getattr(node_type, "primitive_type", None) is not None and \
                node_type.primitive_type.local_name in self.all_types and \
                name in ['СрокДисквЛет', 'СрокДисквМес', 'СрокДисквДн', 'Отправитель', 'ИнвПрич',
                         'Датазаключенияконтракта', 'Датаначала', 'Датаокончания', 'ИНН', 'ИндРейтинг', 'ДатаВыд']:
            logger.trace(f"name: {name}   node_type: {node_type}")
            return self.all_types[node_type.primitive_type.local_name].value(node_type)
        return None

    @staticmethod
    def date_value(pattern):
        return Faker_._fake.date_between_dates(date_start=date(1900, 1, 1), date_end=date(2099, 12, 31)).strftime(
            pattern)
