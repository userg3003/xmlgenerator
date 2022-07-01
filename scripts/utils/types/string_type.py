import random
import string
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_

'''

'''


class StringType():
    name: str = "string"

    def value(self, node_type, sync_attr=None):
        value = None
        length = node_type.get('length', None)
        length = node_type.get('max_length', None) if length is None else length
        length = node_type.get('maxLength', None) if length is None else length
        min_length = node_type.get('min_length', None)
        min_length = node_type.get('min_length', None) if min_length is None else min_length
        if node_type['enumeration'] is not None:
            index = Fake_.random_int(min=0, max=len(node_type['enumeration']) - 1)
            if 'length' in node_type.keys():
                value = node_type['enumeration'][index][:node_type['length']]
            else:
                value = node_type['enumeration'][index]
        if value is None and node_type['patterns'] is not None:
            value = rstr.xeger(node_type['patterns'][0])

        if value is None and length is not None:
            if min_length is not None:
                length = random.randint(min_length, length)
            value = ''.join(random.choices(string.ascii_letters, k=length))

        return value
