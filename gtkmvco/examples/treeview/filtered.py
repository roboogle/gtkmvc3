import gtk

import _importer
import gtkmvc

from filtering import *
import predicates

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
        set_visible_function(self.view['treemodelfilter'],
            get_visible_function([
                ('name', 'contains', "o"),
                ('age', 'lt', 20)
                ], predicates)
            )

m = gtkmvc.Model()
v = gtkmvc.View(builder='filtered.ui')
c = Controller(m, v)

gtk.main()
