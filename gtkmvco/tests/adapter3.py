import unittest

from _importer import refresh_gui

import gtkmvc
from gtkmvc.adapters.containers import StaticContainerAdapter

class Model(gtkmvc.Model):
    box = None
    __observables__ = ["box"]

    def __init__(self):
        gtkmvc.Model.__init__(self)
        self.box = [0, 1, 2]

class Controller(gtkmvc.Controller):
    index = 0

    def on_button3_clicked(self, button):
        self.model.box[self.index] += 1

    on_button4_clicked = on_button3_clicked

class ConnectTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.v = gtkmvc.View(glade="adapters.glade", top="window3")
        self.c = Controller(self.m, self.v)
        refresh_gui()

    def testController(self):
        self.c.adapt("box", "hbox1")
        self.assertStatic()

    def testStatic(self):
        a = StaticContainerAdapter(self.m, "box")
        a.connect_widget(self.v["hbox1"])
        self.assertStatic()

    def assertStatic(self):
        self.assertEqual("0", self.v["entry2"].get_text())
        self.assertEqual("1", self.v["label3"].get_text())
        self.assertEqual("2", self.v["spinbutton1"].get_text())

        self.v["button3"].clicked()
        self.assertEqual("1", self.v["entry2"].get_text())

        self.c.index = 2
        self.v["button3"].clicked()
        self.assertEqual("3", self.v["spinbutton1"].get_text())

        self.v["entry2"].set_text("9")
        self.assertEqual(9, self.m.box[0])

class SetterTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.v = gtkmvc.View(glade="adapters.glade", top="window4")
        self.c = Controller(self.m, self.v)
        refresh_gui()

    def testStatic(self):
        a = StaticContainerAdapter(self.m, "box")
        a.connect_widget(map(lambda x: self.v[x], "en4 lbl4 sb4".split()),
            setters = dict(lbl4=lambda w, v: w.set_markup(
                "<big>Val: <b>%d</b></big>" % v)))

        self.assertEqual("0", self.v["en4"].get_text())
        self.assertEqual("Val: 1", self.v["lbl4"].get_text())
        self.assertEqual("2", self.v["sb4"].get_text())

        self.v["button4"].clicked()
        self.assertEqual("1", self.v["en4"].get_text())

        self.c.index = 2
        self.v["button4"].clicked()
        self.assertEqual("3", self.v["sb4"].get_text())

        self.v["en4"].set_text("9")
        self.assertEqual(9, self.m.box[0])

class DictTest(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.v = gtkmvc.View(glade="adapters.glade", top="window4")
        self.c = Controller(self.m, self.v)
        refresh_gui()
        self.m.box = dict(en4=0, lbl4=1, sb4=2)
        self.c.index = "en4"

    def testStatic(self):
        a = StaticContainerAdapter(self.m, "box")
        a.connect_widget(map(lambda x: self.v[x], "en4 lbl4 sb4".split()),
            setters = dict(lbl4=lambda w, v: w.set_markup(
                "<big>Val: <b>%d</b></big>" % v)))

        self.assertEqual("0", self.v["en4"].get_text())
        self.assertEqual("Val: 1", self.v["lbl4"].get_text())
        self.assertEqual("2", self.v["sb4"].get_text())

        self.v["button4"].clicked()
        self.assertEqual("1", self.v["en4"].get_text())

        self.c.index = "sb4"
        self.v["button4"].clicked()
        self.assertEqual("3", self.v["sb4"].get_text())

        self.v["en4"].set_text("9")
        self.assertEqual(9, self.m.box["en4"])

if __name__ == "__main__":
    unittest.main()
