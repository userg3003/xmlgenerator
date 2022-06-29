import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class SnilsType():
    name: str = "СНИЛСТип"

    def value(self, node_type):
        div = Fake_.random_element(elements=(' ', '-'))
        value = Fake_.numerify(text=f"###-###-###{div}##")
        return value
