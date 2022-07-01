import random
import rstr
import string
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class OKSMType():
    name: str = "ОКСМТип"

    def value(self, node_type, sync_attr=None):
        value = get_oksm(node_type)
        return value


def get_oksm(node_type):
    value = None
    length = node_type.get('length', None)
    length = node_type.get('max_length', None) if length is None else length
    length = node_type.get('maxLength', None) if length is None else length
    if node_type.get('enumeration', None) is not None:
        index = Fake_.random_int(min=0, max=len(node_type['enumeration']) - 1)
        if node_type['length'] is not None:
            value = node_type['enumeration'][index][:length]
        else:
            value = node_type['enumeration'][index]

    if node_type.get('patterns', None) is not None:
        value = rstr.xeger(node_type['patterns'][0])
    if value is None and length is not None:
        value = ''.join(random.choices(string.ascii_letters, k=length))
    # else:
    #     pattern = "#" * 2
    #     value = Fake_.numerify(text=pattern)
    return value
