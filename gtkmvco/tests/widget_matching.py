"""
Test should print:
overridden
ValueError: Widget 'prop' not found

This verifies that subclasses can override the way Controller matches widget
name for adaption.
"""

import gtk

import _importer
import gtkmvc

class Model(gtkmvc.Model):
    prop = None
    __observables__ = ("prop",)

class Foo(gtkmvc.Controller):
    def register_adapters(self):
        self.adapt("prop")

    def _find_widget_match(self, prop_name):
        print "overridden"
        return prop_name

m = Model()
v = gtkmvc.View()
c = Foo(m, v)

gtk.main()
