from loguru import logger
from datetime import date
from scripts.utils.attributes.attributes import Faker_
from scripts.utils.attributes.misc import PhoneNumber, Job, Email, KolDok
from scripts.utils.attributes.dates import Year, Month, Day
from scripts.utils.attributes.inn import InnFL, InnYL, Inn
from scripts.utils.attributes.fid import Fid
from scripts.utils.attributes.position import CityName, Region, StreetName, BuildingNumber, BuildingHouse, Quarter, \
    Locality, BirthPlace
from scripts.utils.attributes.fio import LastName, FirstName, MiddleName
from scripts.utils.types.number_abonent import NumberAbonentType
from scripts.utils.types.integer_type import IntegerType, LongType, IntType
from scripts.utils.types.decimal_type import DecimalType
from scripts.utils.types.snils import SnilsType
from scripts.utils.types.string_type import StringType
from scripts.utils.types.data_type import DataType, DataYmdType, DataNType, Date
from scripts.utils.types.inn import InnFLType, InnYLType
from scripts.utils.types.oksm import OKSMType
from scripts.utils.types.test_type import TESTType
from scripts.utils.types.spdul import SPDULType, SPDULschType
from scripts.utils.xml_utils import get_all_value_from_facet


# from scripts.utils.types import Fake_


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
        self.all_faker[KolDok.name] = KolDok()
        self.all_faker[Month.name] = Month()
        self.all_faker[Day.name] = Day()
        self.all_faker[Year.name] = Year()
        self.all_faker[InnFL.name] = InnFL()  # InnFL, InnYL, Inn
        self.all_faker[InnYL.name] = InnYL()
        self.all_faker[Inn.name] = Inn()
        self.all_faker[Fid.name] = Fid()
        self.all_types = dict()
        self.all_types[NumberAbonentType.name] = NumberAbonentType()
        self.all_types[IntegerType.name] = IntegerType()
        self.all_types[LongType.name] = LongType()
        self.all_types[IntType.name] = IntType()
        self.all_types[DecimalType.name] = DecimalType()
        self.all_types[StringType.name] = StringType()
        self.all_types[SnilsType.name] = SnilsType()
        self.all_types[DataType.name] = DataType()
        self.all_types[Date.name] = Date()
        self.all_types[DataYmdType.name] = DataYmdType()
        self.all_types[DataNType.name] = DataNType()
        self.all_types[InnFLType.name] = InnFLType()
        self.all_types[InnYLType.name] = InnYLType()
        self.all_types[OKSMType.name] = OKSMType()
        self.all_types[TESTType.name] = TESTType()
        self.all_types[SPDULType.name] = SPDULType()
        self.all_types[SPDULschType.name] = SPDULschType()

    def value(self, name, node_type=None, sync_attr=None):
        logger.debug(
            f"name: {name}   node_type: {node_type} node_type.local_name {node_type.local_name if node_type is not None else None}")
        value = None
        merged_types = self.all_facets(node_type)

        if "Пр" not in name and 'Дата' in name and getattr(node_type, "local_name", None) not in ["date", 'ДатаТип',
                                                                                                  'Дата_ГГГГММДД',
                                                                                                  'ДатаНТип']:
            logger.trace(f"name: {name}   node_type: {node_type}")
            return self.date_value("%d.%m.%Y")
        elif name in self.all_faker.keys():
            logger.trace(f"name: {name}   node_type: {node_type}")
            value = self.all_faker[name].value(merged_types, sync_attr)
        elif merged_types['name'] in self.all_types:
            logger.trace(f"name: {name}   node_type: {node_type}")
            value = self.all_types[merged_types['name']].value(merged_types, sync_attr)
        elif name in ['СрокДисквЛет', 'СрокДисквМес', 'СрокДисквДн', 'Отправитель', 'ИнвПрич',
                         'Датазаключенияконтракта', 'Датаначала', 'Датаокончания', 'ИНН', 'ИндРейтинг',
                         'ИдЕРН', 'ДатаСвед', 'ПрПодп', 'Код', 'Тип', 'КПП', 'ДатаКонДискв',
                         'ДатаОсвоб', 'ДатаВСилу', 'ДатаАрест', 'ДатаЦиркРоз', 'ДатаИзменРоз', 'Индекс',
                         'КодРегион', 'ДоляПроц']:
            logger.trace(f"name: {name}   node_type: {node_type}")
            value = self.all_types[merged_types["local_name"]].value(merged_types, sync_attr)
        elif "Пр" not in name and 'Дата' in name and getattr(node_type, "local_name", None) != "date":
            logger.trace(f"name: {name}   node_type: {node_type}")
            value = self.date_value("%d.%m.%Y")
        return value

    @staticmethod
    def date_value(pattern):
        return Faker_._fake.date_between_dates(date_start=date(1900, 1, 1), date_end=date(2099, 12, 31)).strftime(
            pattern)

    @staticmethod
    def all_facets(node_type):
        # value = Fake_.numerify(text=f"{'#'*{facts_values['length']}")
        all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
        logger.trace(f" node_type: {node_type}")
        type_ = dict()
        node_name = "node_type"
        type_[node_name] = Fakers.all_facets_fot_type(node_name, node_type)
        logger.trace(f"node_name {node_name}")
        node_name = "base_type"
        type_[node_name] = Fakers.get_facets(node_name, node_type)
        logger.trace(f"node_name {node_name}")
        node_name = "primitive_type"
        type_[node_name] = Fakers.get_facets(node_name, node_type)
        logger.trace(f"node_name {node_name}")
        node_name = "member_types"
        type_[node_name] = Fakers.get_facets(node_name, node_type)
        logger.trace(f"node_name {node_name}")

        # Объеденить типы
        merged_type = dict()
        for key in type_["node_type"]:
            if type_["node_type"][key] is not None:
                merged_type[key] = type_["node_type"][key]
            elif type_["primitive_type"] is not None and type_["primitive_type"].get(key, None) is not None:
                merged_type[key] = type_["primitive_type"][key]
            elif type_["base_type"] is not None and type_["base_type"].get(key, None) is not None:
                merged_type[key] = type_["base_type"][key]
            elif type_["member_types"] is not None and type_["member_types"].get(key, None) is not None:
                merged_type[key] = type_["member_types"][key]
            else:
                merged_type[key] = None
        Fakers.add_keys(merged_type, type_, "primitive_type")
        Fakers.add_keys(merged_type, type_, "base_type")
        Fakers.add_keys(merged_type, type_, "member_types")

        if merged_type["local_name"] not in ["string", "decimal", "float", "int", "integer", "boolean", "data", "time",
                                             "duration", "gYear", "gMonth",
                                             "dataTime"]:
            if type_["primitive_type"] is not None:
                if type_["primitive_type"].get("name", None) is not None:
                    merged_type["local_name"] = type_["primitive_type"]["name"]
                if type_["primitive_type"].get("local_name", None) is not None:
                    merged_type["local_name"] = type_["primitive_type"]["local_name"]

            elif type_["base_type"] is not None:
                if type_["base_type"].get("name", None) is not None:
                    merged_type["local_name"] = type_["base_type"]["name"]
                if type_["base_type"].get("local_name", None) is not None:
                    merged_type["local_name"] = type_["base_type"]["local_name"]
            elif type_["primitive_type"] is not None:
                if type_["primitive_type"].get("name", None) is not None:
                    merged_type["local_name"] = type_["primitive_type"]["name"]
                if type_["primitive_type"].get("local_name", None) is not None:
                    merged_type["local_name"] = type_["primitive_type"]["local_name"]
            elif type_["member_types"] is not None:
                if type_["member_types"].get("name", None) is not None:
                    merged_type["local_name"] = type_["member_types"]["name"]
                if type_["member_types"].get("local_name", None) is not None:
                    merged_type["local_name"] = type_["member_types"]["local_name"]
        if merged_type['name'] is None:
            merged_type['name'] = "string"
        if merged_type['local_name'] is None:
            merged_type['name'] = "string"
        return merged_type

    @staticmethod
    def add_keys(merged_type, type_, name):
        if type_[name] is not None:
            for key in type_[name].keys():
                if key not in merged_type.keys():
                    merged_type[key] = type_[name][key]

    @staticmethod
    def get_facets(node_name, node_type):
        type_ = None
        base_type = getattr(node_type, node_name, None)
        if base_type is not None:
            if isinstance(base_type, list):
                types = dict()
                for i, item in enumerate(base_type):
                    t = Fakers.all_facets_fot_type(f"member {i}", item)
                    if i > 0:
                        for key in t.keys():
                            if t[key] is not None and types.get(key, None) is None:
                                types[key] = t[key]
                    else:
                        types = t
                if types != dict():
                    type_ = types
                logger.trace(f"")
            else:
                type_ = Fakers.all_facets_fot_type(node_name, base_type)
        return type_

    @staticmethod
    def all_facets_fot_type(node_name, node_type):
        type_ = dict()
        logger.trace(f" node_name {node_name}   node_type: {node_type}")
        for attr in node_type.facets:
            if attr is not None:
                attr_name = attr.split("}")[1]
                type_[attr_name] = getattr(node_type.facets[attr], "value", None)
        name_attr = "name"
        name = getattr(node_type, name_attr, None)
        if name is not None:
            nn = name.split("}")
            type_[name_attr] = name.split("}")[1] if len(nn) > 1 else nn[0]
        else:
            type_[name_attr] = None
        type_["local_name"] = getattr(node_type, "local_name", None)
        type_["max_length"] = getattr(node_type, "max_length", None)
        type_["min_length"] = getattr(node_type, "min_length", None)
        type_["max_value"] = getattr(node_type, "max_value", None)
        type_["min_value"] = getattr(node_type, "min_value", None)
        type_["pattern"] = getattr(node_type, "pattern", None)
        patterns = getattr(node_type, "patterns", None)
        type_["patterns"] = getattr(patterns, "regexps", None) if patterns is not None else None

        type_["enumeration"] = getattr(node_type, "enumeration", None)

        return type_
