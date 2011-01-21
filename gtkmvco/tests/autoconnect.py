"""
Test shows a button. Clicking it should print. Closing the window should quit
the program.

This tests recognizing handlers by name instead of defining them in Glade.

TODO unittest, class attribute
"""

import gtk

import _importer
import gtkmvc

class View(gtkmvc.View):
    def __init__(self):
        gtkmvc.View.__init__(self)

        w = self['window'] = gtk.Window()
        b = self['button_doit'] = gtk.Button("OK")
        w.add(b)
        w.show_all()

class Super(gtkmvc.Controller):
    def on_window__delete_event(self, window, event):
        gtk.main_quit()

class Controller(Super):
    def on_button_doit__clicked(self, button):
        print "Ouch!"

m = gtkmvc.Model()
v = View()
c = Controller(m, v, handlers="class")

gtk.main()
