import random

from scripts.utils.attributes.attributes import Faker_


class PhoneNumber(Faker_):
    name: str = "Тлф"

    @property
    def value(self):
        return Faker_._fake.phone_number()


class Job(Faker_):
    name: str = "ДолжОтв"

    @property
    def value(self):
        return Faker_._fake.job()


class Email(Faker_):
    name: str = "E-mail"

    @property
    def value(self):
        return Faker_._fake.email()


class KolDok(Faker_):
    name: str = "КолДок"

    @property
    def value(self):
        return str(random.randrange(1, 1000))
