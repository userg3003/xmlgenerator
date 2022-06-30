from scripts.utils.attributes.attributes import Faker_


class LastName(Faker_):
    name: str = "Фамилия"

    def value(self, node_type=None, param=None):
        return Faker_._fake.last_name()


class FirstName(Faker_):
    name: str = "Имя"

    def value(self, node_type=None, param=None):
        return Faker_._fake.first_name()


class MiddleName(Faker_):
    name: str = "Отчество"

    def value(self, node_type=None, param=None):
        return Faker_._fake.middle_name()
