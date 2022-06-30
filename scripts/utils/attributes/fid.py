from loguru import logger
from scripts.utils.attributes.attributes import Faker_
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_


class Fid(Faker_):
    name: str = "ФИД"

    def value(self, node_type=None, param=None):
        value = Faker_._fake.last_name()
        value = Fid.get_fid(node_type, param)
        logger.debug(f"{Fid.name} value: {value} param: {param}")
        return value

    @staticmethod
    def get_fid(node_type, param):
        logger.debug(f"{node_type}  param: {param}")
        if node_type is None:
            return "ФИД ТИП None"
        all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
        type_ = dict()
        for attr in all_facets_types:
            type_[attr] = get_value_from_facet(node_type.facets, attr)
        totalDigits = type_['totalDigits'] if 'totalDigits' in type_.keys() else 10
        # length = type_['length'] if 'length' in type_.keys() else 10
        # length = type_['maxLength'] if 'maxLength' in type_.keys() else length
        # pattern = "#" * length
        # value = Fake_.numerify(text=pattern)
        # value=format(param, f"0{length}d")
        value=str(param)
        return value
