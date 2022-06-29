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
