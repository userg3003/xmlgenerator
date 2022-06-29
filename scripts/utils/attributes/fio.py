from scripts.utils.attributes.attributes import Faker_


class LastName(Faker_):
    name: str = "Фамилия"

    @property
    def value(self):
        return Faker_._fake.last_name()


class FirstName(Faker_):
    name: str = "Имя"

    @property
    def value(self):
        return Faker_._fake.first_name()


class MiddleName(Faker_):
    name: str = "Отчество"

    @property
    def value(self):
        return Faker_._fake.middle_name()
