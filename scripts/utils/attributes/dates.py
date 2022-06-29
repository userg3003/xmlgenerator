from scripts.utils.attributes.attributes import Faker_


class Year(Faker_):
    name: str = "Год"

    @property
    def value(self):
        return Faker_._fake.year()


class Month(Faker_):
    name: str = "Месяц"

    @property
    def value(self):
        return Faker_._fake.month()


class Day(Faker_):
    name: str = "День"

    @property
    def value(self):
        return Faker_._fake.day_of_month()
