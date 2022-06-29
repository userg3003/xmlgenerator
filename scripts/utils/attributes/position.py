from scripts.utils.attributes.attributes import Faker_


class CityName(Faker_):
    name: str = "Город"

    @property
    def value(self):
        return Faker_._fake.city_name()


class Region(Faker_):
    name: str = "Район"

    @property
    def value(self):
        return Faker_._fake.city()


class StreetName(Faker_):
    name: str = "Улица"

    @property
    def value(self):
        return Faker_._fake.street_name()


class BuildingNumber(Faker_):
    name: str = "Дом"

    @property
    def value(self):
        return Faker_._fake.building_number()


class BuildingHouse(Faker_):
    name: str = "Корпус"

    @property
    def value(self):
        return Faker_._fake.building_number()


class Quarter(Faker_):
    name: str = "Кварт"

    @property
    def value(self):
        return Faker_._fake.building_number()


class Locality(Faker_):
    name: str = "НаселПункт"

    @property
    def value(self):
        return Faker_._fake.city()


class BirthPlace(Faker_):
    name: str = "МестоРожд"

    @property
    def value(self):
        return f"{Faker_._fake.administrative_unit()}, {Faker_._fake.city()}"
