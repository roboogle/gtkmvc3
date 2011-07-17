import gtk

import _importer
import gtkmvc

class Person(gtkmvc.Model):
    name = ''
    __observables__ = ('name',)

class Controller(gtkmvc.Controller):
    def register_adapters(self):
        gtkmvc.adapters.containers.watch_items_in_tree(self.view['liststore1'])
        self.setup_columns()

    def on_add_clicked(self, button):
        t = self.view['liststore1']
        m = Person()
        v = gtkmvc.View(builder='single.ui')
        c = gtkmvc.Controller(m, v, auto_adapt=True)
        t.append([m])

    def on_remove_clicked(self, button):
        # TODO move object lookup into view method.
        t, i = self.view['treeview1'].get_selection().get_selected()
        t.remove(i)

m = gtkmvc.Model()
v = gtkmvc.View(builder='update.ui')
c = Controller(m, v)

gtk.main()
