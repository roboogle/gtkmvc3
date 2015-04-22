import _importer

import gtkmvc3

class Person(gtkmvc3.Model):
    __observables__ = ('name', 'age')

    @gtkmvc3.Model.getter('*')
    def calculate(self, name):
        return 0

assert Person().name == 0
