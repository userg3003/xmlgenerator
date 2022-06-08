import random
from faker import Faker
from faker.providers import date_time, internet, lorem, person, python

random.seed()
Faker.seed(random.randint(1, 100))


def make_fake():
    fake = Faker("ru_RU")
    fake.add_provider(person)
    fake.add_provider(internet)
    fake.add_provider(python)
    fake.add_provider(date_time)
    return fake


class Faker:
    _fake = make_fake()

    def __init__(self):
        self._name = None
        self._value = None

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


class LastName(Faker):
    name: str = "Фамилия"

    @property
    def value(self):
        return Faker._fake.last_name()


class FirstName(Faker):
    name: str = "Имя"

    @property
    def value(self):
        return Faker._fake.first_name()


class MiddleName(Faker):
    name: str = "Отчество"

    @property
    def value(self):
        return Faker._fake.middle_name()


class CityName(Faker):
    name: str = "Город"

    @property
    def value(self):
        return Faker._fake.city_name()


class PhoneNumber(Faker):
    name: str = "Тлф"

    @property
    def value(self):
        return Faker._fake.phone_number()


class Region(Faker):
    name: str = "Район"

    @property
    def value(self):
        return Faker._fake.city()


#
class StreetName(Faker):
    name: str = "Улица"

    @property
    def value(self):
        return Faker._fake.street_name()


#
class BuildingNumber(Faker):
    name: str = "Дом"

    @property
    def value(self):
        return Faker._fake.building_number()


#
class BuildingHouse(Faker):
    name: str = "Корпус"

    @property
    def value(self):
        return Faker._fake.building_number()


#
class Quarter(Faker):
    name: str = "Кварт"

    @property
    def value(self):
        return Faker._fake.building_number()


#
class Job(Faker):
    name: str = "ДолжОтв"

    @property
    def value(self):
        return Faker._fake.job()


class Email(Faker):
    name: str = "E-mail"

    @property
    def value(self):
        return Faker._fake.email()


class Locality(Faker):
    name: str = "НаселПункт"

    @property
    def value(self):
        return Faker._fake.city()


class BirthPlace(Faker):
    name: str = "МестоРожд"

    @property
    def value(self):
        return f"{Faker._fake.administrative_unit()}, {Faker._fake.city()}"


class Year(Faker):
    name: str = "Год"

    @property
    def value(self):
        return Faker._fake.year()


class Month(Faker):
    name: str = "Месяц"

    @property
    def value(self):
        return Faker._fake.month()


class Day(Faker):
    name: str = "День"

    @property
    def value(self):
        return Faker._fake.day_of_month()


class KolDok(Faker):
    name: str = "КолДок"

    @property
    def value(self):
        return str(random.randrange(1, 1000))


class Fakers:
    def __init__(self):
        self.all_faker = dict()
        self.all_faker[LastName.name] = LastName()
        self.all_faker[FirstName.name] = FirstName()
        self.all_faker[MiddleName.name] = MiddleName()
        self.all_faker[CityName.name] = CityName()
        self.all_faker[PhoneNumber.name] = PhoneNumber()
        self.all_faker[Region.name] = Region()
        self.all_faker[StreetName.name] = StreetName()
        self.all_faker[BuildingNumber.name] = BuildingNumber()
        self.all_faker[BuildingHouse.name] = BuildingHouse()
        self.all_faker[Quarter.name] = Quarter()
        self.all_faker[Job.name] = Job()
        self.all_faker[Email.name] = Email()
        self.all_faker[Locality.name] = Locality()
        self.all_faker[BirthPlace.name] = BirthPlace()
        self.all_faker[KolDok.name] = Email()
        self.all_faker[Month.name] = Month()
        self.all_faker[Day.name] = Day()
        self.all_faker[Year.name] = Year()

    def value(self, name):
        if name in self.all_faker.keys():
            return self.all_faker[name].value
        else:
            return None
