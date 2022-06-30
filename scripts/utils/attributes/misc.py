import random

from scripts.utils.attributes.attributes import Faker_


class PhoneNumber(Faker_):
    name: str = "Тлф"

    def value(self, node_type=None, param=None):
        return Faker_._fake.phone_number()


class Job(Faker_):
    name: str = "ДолжОтв"

    def value(self, node_type=None, param=None):
        return Faker_._fake.job()


class Email(Faker_):
    name: str = "E-mail"

    def value(self, node_type=None, param=None):
        return Faker_._fake.email()


class KolDok(Faker_):
    name: str = "КолДок"

    def value(self, node_type=None, param=None):
        return str(random.randrange(1, 1000))
