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

    def value(self, node_type):
        value = Fake_.date_between_dates(date_start=date(1900, 1, 1), date_end=date(2099, 12, 31)).strftime(
            "%d.%m.%Y")
        return value
