from loguru import logger
from datetime import date
from scripts.utils.attributes.attributes import Faker_
from scripts.utils.attributes.misc import PhoneNumber, Job, Email, KolDok
from scripts.utils.attributes.dates import Year, Month, Day
from scripts.utils.attributes.position import CityName, Region, StreetName, BuildingNumber, BuildingHouse, Quarter, \
    Locality, BirthPlace
from scripts.utils.attributes.fio import LastName, FirstName, MiddleName
from scripts.utils.types.number_abonent import NumberAbonentType
from scripts.utils.types.integer_type import IntegerType, LongType, IntType
from scripts.utils.types.decimal_type import DecimalType
from scripts.utils.types.snils import SnilsType
from scripts.utils.types.string_type import StringType
from scripts.utils.types.data_type import DataType, DataTypeYmd
from scripts.utils.types.inn import InnFLType, InnYLType


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
        self.all_types[DataTypeYmd.name] = DataTypeYmd()
        self.all_types[InnFLType.name] = InnFLType()
        self.all_types[InnYLType.name] = InnYLType()

    def value(self, name, node_type=None):
        logger.trace(
            f"name: {name}   node_type: {node_type} node_type.local_name {node_type.local_name if node_type is not None else None}")
        value = None
        if "Пр" not in name and 'Дата' in name and getattr(node_type, "local_name", None) not in ["date", 'ДатаТип',
                                                                                                  'Дата_ГГГГММДД']:
            logger.trace(f"name: {name}   node_type: {node_type}")
            return self.date_value("%d.%m.%Y")
        elif name in self.all_faker.keys():
            logger.trace(f"name: {name}   node_type: {node_type}")
            value = self.all_faker[name].value
        elif node_type.local_name in self.all_types:
            logger.trace(f"name: {name}   node_type: {node_type}")
            value = self.all_types[node_type.local_name].value(node_type)
        elif getattr(node_type, "primitive_type", None) is not None and \
                node_type.primitive_type.local_name in self.all_types and \
                name in ['СрокДисквЛет', 'СрокДисквМес', 'СрокДисквДн', 'Отправитель', 'ИнвПрич',
                         'Датазаключенияконтракта', 'Датаначала', 'Датаокончания', 'ИНН', 'ИндРейтинг',
                         'ИдЕРН', 'ДатаСвед', 'ПрПодп', 'Код', 'Тип', 'КПП', 'ДатаКонДискв',
                         'ДатаОсвоб', 'ДатаВСилу', 'ДатаАрест', 'ДатаЦиркРоз', 'ДатаИзменРоз', 'Индекс',
                         'КодРегион']:
            logger.trace(f"name: {name}   node_type: {node_type}")
            value = self.all_types[node_type.primitive_type.local_name].value(node_type)
        elif "Пр" not in name and 'Дата' in name and getattr(node_type, "local_name", None) != "date":
            logger.trace(f"name: {name}   node_type: {node_type}")
            value = self.date_value("%d.%m.%Y")
        return value

    @staticmethod
    def date_value(pattern):
        return Faker_._fake.date_between_dates(date_start=date(1900, 1, 1), date_end=date(2099, 12, 31)).strftime(
            pattern)
