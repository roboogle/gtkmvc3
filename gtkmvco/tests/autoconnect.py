import unittest

from gi.repository import Gtk, Gdk

from _importer import refresh_gui
import gtkmvc3

class Super(gtkmvc3.Controller):
    def __init__(self, **kwargs):
        self.calls = []

        v = gtkmvc3.View()
        v['main_window'] = w = Gtk.Window()
        v['button'] = b = Gtk.Button()
        w.add(b)

        gtkmvc3.Controller.__init__(self, gtkmvc3.Model(), v, **kwargs)
        refresh_gui()

    def on_button__clicked(self, widget):
        self.calls.append(widget)

class Controller(Super):
    handlers = "class"

    def on_main_window__delete_event(self, widget, event):
        self.calls.append(widget)

class AutoConnect(unittest.TestCase):
    def testDefault(self):
        c = Super()
        w = c.view['button']
        w.clicked()
        self.assertEqual([], c.calls)

    def testArgument(self):
        c = Super(handlers="class")
        w = c.view['button']
        w.clicked()
        self.assertEqual([w], c.calls)

    def testAttribute(self):
        c = Controller()
        w = c.view['button']
        w.clicked()
        self.assertEqual([w], c.calls)

    def testUnderscores(self):
        c = Controller()
        w = c.view['main_window']
        # Didn't find a better way.
        w.emit('delete-event', Gdk.Event())
        self.assertEqual([w], c.calls)

if __name__ == "__main__":
    unittest.main()
