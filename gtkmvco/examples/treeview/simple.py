import gtk

import _importer
import gtkmvc

class Person(gtkmvc.Model):
    name = ''
    age = 0
    license = False
    __observables__ = ('name', 'age')

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        m = view['liststore1']

        p = Person()
        p.name = 'Joe'
        p.age = 15
        m.append([p])

        p = Person()
        p.name = 'Mary'
        p.age = 60
        p.license = True
        m.append([p])

    def register_adapters(self):
        self.setup_columns()

m = gtkmvc.Model()
v = gtkmvc.View(builder='simple.ui')
c = Controller(m, v)

gtk.main()
