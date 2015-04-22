import unittest

from gi.repository import Gtk

from _importer import refresh_gui

import gtkmvc3

class Model(gtkmvc3.Model):
    title = ''
    __observables__ = ['title']

class Controller(gtkmvc3.Controller):
    def register_view(self, view):
        view['window'] = Gtk.Window()

    def register_adapters(self):
        self.adapt('title', 'window', 'title')

class PropertyAdapter(unittest.TestCase):
    def testConnection(self):
        m = Model()
        v = gtkmvc3.View()
        c = Controller(m, v)
        refresh_gui()
        self.assertEqual(m.title, v['window'].get_title())
        m.title = "Hello"
        self.assertEqual(m.title, v['window'].get_title())
        v['window'].set_title("World")
        self.assertEqual(m.title, v['window'].get_title())

if __name__ == '__main__':
    unittest.main()
