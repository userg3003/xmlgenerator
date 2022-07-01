from datetime import date
from scripts.utils.attributes.attributes import Faker_


class Year(Faker_):
    name: str = "Год"

    def value(self, node_type=None, param=None):
        return Faker_._fake.year()


class Month(Faker_):
    name: str = "Месяц"

    def value(self, node_type=None, param=None):
        return Faker_._fake.month()


class Day(Faker_):
    name: str = "День"

    def value(self, node_type=None, param=None):
        return Faker_._fake.day_of_month()


