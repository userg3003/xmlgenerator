import random
import rstr
import string
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class SPDULType():
    name: str = 'СПДУЛТип'

    def value(self, node_type, sync_attr=None):
        value = get_spdul(node_type)
        return value


def get_spdul(node_type):
    length = node_type.get('length', None)
    length = node_type.get('max_length', None) if node_type.get('max_length', None) is not None else length
    value = None
    if node_type['enumeration'] is not None:
        index = Fake_.random_int(min=0, max=len(node_type['enumeration']) - 1)
        if length is not None:
            value = node_type['enumeration'][index][:node_type['length']]
        else:
            value = node_type['enumeration'][index]
    if value is None and node_type['patterns'] is not None:
        value = rstr.xeger(node_type['patterns'][0])
    if value is None and length is not None:
        value = ''.join(random.choices(string.ascii_letters, k=length))
    if value is None:
        pattern = "#" * 2
        value = Fake_.numerify(text=pattern)
    return value


class SPDULschType():
    name: str = 'СПДУЛШТип'

    def value(self, node_type, sync_attr=None):
        value = get_spdul(node_type)
        return value
