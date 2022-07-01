from datetime import date
import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_

'''

'''


class DataType():
    name: str = "ДатаТип"

    def value(self, node_type, sync_attr=None):
        value = None
        if node_type.get('enumeration', None) is not None:
            index = Fake_.random_int(min=0, max=len(node_type['enumeration']) - 1)
            if node_type['length'] is not None:
                value = node_type['enumeration'][index][:node_type['length']]
            else:
                value = node_type['enumeration'][index]

        if node_type.get('patterns', None) is not None:
            value = rstr.xeger(node_type['patterns'][0])
        if value is None:
            value = Fake_.date_between_dates(date_start=date(1900, 1, 1), date_end=date(2099, 12, 31)).strftime(
                "%d.%m.%Y")
        return value


class DataYmdType():
    name: str = "Дата_ГГГГММДД"

    def value(self, node_type, sync_attr=None):
        if node_type['enumeration'] is not None:
            index = Fake_.random_int(min=0, max=len(node_type['enumeration']) - 1)
            if node_type['length'] is not None:
                value = node_type['enumeration'][index][:node_type['length']]
            else:
                value = node_type['enumeration'][index]

        if node_type['patterns'] is not None:
            value = rstr.xeger(node_type['patterns'][0])
        if value is None:
            value = Fake_.date_between_dates(date_start=date(1900, 1, 1), date_end=date(2099, 12, 31)).strftime(
                "%Y.%m.%d")
        return value


class DataNType():
    name: str = "ДатаНТип"

    def value(self, node_type, sync_attr=None):
        if node_type['enumeration'] is not None:
            index = Fake_.random_int(min=0, max=len(node_type['enumeration']) - 1)
            if node_type['length'] is not None:
                value = node_type['enumeration'][index][:node_type['length']]
            else:
                value = node_type['enumeration'][index]

        if node_type['patterns'] is not None:
            value = rstr.xeger(node_type['patterns'][0])
        if value is None:
            value = Fake_.date_between_dates(date_start=date(1900, 1, 1), date_end=date(2099, 12, 31)).strftime(
                "%Y.%m.%d")
        return value


class Date():
    name: str = "date"

    def value(self, node_type=None, param=None):
        # return self.date_value("%d.%m.%Y")
        return self.date_value("%Y-%m-%d")

    def date_value(self, pattern):
        return Fake_.date_between_dates(date_start=date(1900, 1, 1), date_end=date(2099, 12, 31)).strftime(
            pattern)
