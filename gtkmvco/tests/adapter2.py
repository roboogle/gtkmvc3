import unittest

from _importer import refresh_gui

import gtkmvc
from gtkmvc.adapters.basic import UserClassAdapter
from gtkmvc import observable

class UserClass (observable.Observable):
    def __init__(self, max_val):
        observable.Observable.__init__(self)
        self.x = 0
        self.max_val = max_val
        return

    @observable.observed
    def set_x(self, v):
        if v > self.max_val:
            raise ValueError("x cannot be greater than %d" % self.max_val)
        self.x=v
        return
        
    def get_x(self): return self.x
    pass

class Model(gtkmvc.Model):
    x = UserClass(10)
    __observables__ = ["x"]

class Controller(gtkmvc.Controller):
    caught = False

    def on_button2_clicked(self, button):
        try:
            self.model.x.set_x(self.model.x.get_x() + 1)
        except ValueError:
            self.caught = True

class User(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.v = gtkmvc.View(glade="adapters.glade", top="window2")
        self.c = Controller(self.m, self.v)
        refresh_gui()

    def testArguments(self):
        errors = []
        def handle(adapter, name, value):
            errors.append((adapter, name, value))
            adapter.update_widget()

        a = UserClassAdapter(self.m, "x", "get_x", "set_x", value_error=handle)
        a.connect_widget(self.v["en2"])

        self.assertEqual("0", self.v["en2"].get_text())

        self.v["button2"].clicked()
        self.assertEqual("1", self.v["en2"].get_text())

        self.m.x.set_x(10)
        self.assertEqual("10", self.v["en2"].get_text())

        self.assertFalse(self.c.caught)
        self.v["button2"].clicked()
        self.assertTrue(self.c.caught)

        self.v["en2"].set_text("11")
        self.assertEqual((a, "x", "11"), errors[-1])

if __name__ == "__main__":
    unittest.main()
