from scripts.utils.attributes.attributes import Faker_


class CityName(Faker_):
    name: str = "Город"

    def value(self, node_type=None, param=None):
        return Faker_._fake.city_name()


class Region(Faker_):
    name: str = "Район"

    def value(self, node_type=None, param=None):
        return Faker_._fake.city()


class StreetName(Faker_):
    name: str = "Улица"

    def value(self, node_type=None, param=None):
        return Faker_._fake.street_name()


class BuildingNumber(Faker_):
    name: str = "Дом"

    def value(self, node_type=None, param=None):
        return Faker_._fake.building_number()


class BuildingHouse(Faker_):
    name: str = "Корпус"

    def value(self, node_type=None, param=None):
        return Faker_._fake.building_number()


class Quarter(Faker_):
    name: str = "Кварт"

    def value(self, node_type=None, param=None):
        return Faker_._fake.building_number()


class Locality(Faker_):
    name: str = "НаселПункт"

    def value(self, node_type=None, param=None):
        return Faker_._fake.city()


class BirthPlace(Faker_):
    name: str = "МестоРожд"

    def value(self, node_type=None, param=None):
        return f"{Faker_._fake.administrative_unit()}, {Faker_._fake.city()}"
