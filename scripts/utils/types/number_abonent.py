import random
import rstr
from loguru import logger
from scripts.utils.xml_utils import get_value_from_facet
from scripts.utils.types import Fake_

'''
Генерация номера абонента (тип НомерАбонентТип)
По паттерну из xsd: '^(?:(?:(?:\\+7|7|8)+(?:[0-9]){10}))$(?!\\n\\Z)'
генерируется значение (образец):
'8788888777+7878+7+78+7+7+787+778+7788+787+77+778+7+7+7+7788+78+7+77777+7878+7887+7+78+7788+78887788788+7+777+79871923912'
В связи с этим, значение генерируется не по паттерну, а сонкатенацией префикса (случайный выбор из 3-ч возможных 
значений: "+7", "7", "8") и десятизначного числа.
При импорте атрибута с типом НомерАбонентТип значения minLength и maxLength не учитываются.

'''


class NumberAbonentType():
    name: str = "НомерАбонентТип"

    def value(self, node_type, sync_attr=None):
        pref = Fake_.random_element(elements=('+7', '7', '8'))
        digits = Fake_.numerify(text="##########")
        value = f"{pref}{digits}"
        return value
