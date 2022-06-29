from scripts import utils as util


class Faker_:
    _fake = util.make_fake()

    def __init__(self):
        self._name = None
        self._value = None

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


