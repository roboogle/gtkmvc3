"""
Test for getter and setter decorators, used in models to define 
logical properties
"""

import _importer
from gtkmvc import Model
from gtkmvc.support import metaclasses

import unittest

class MyModel (Model):

    __observables__ = ("prop1", "prop2", "prop3")

    @Model.getter
    def get_prop1(self): return 0
    
    @Model.setter
    def set_prop1(self, val): return

    @Model.getter("prop2", "prop3")
    def getter_for_props(self, name): return name

    @Model.setter("prop2")
    def setter_for_prop2(self, name, val): return

    @Model.setter("prop3")
    def setter_for_prop3(self, name, val): return

    pass # end of class
# ----------------------------------------------------------------------


class LogicalProps(unittest.TestCase):
    def setUp(self): 
        return
        
    def test_prop1_markers(self):
        self.assertEqual(getattr(MyModel.get_prop1, 
                                 metaclasses.GETTER_SETTER_ATTR_MARKER),
                         metaclasses.GETTER_NOARGS_MARKER)

        self.assertEqual(getattr(MyModel.set_prop1, 
                                 metaclasses.GETTER_SETTER_ATTR_MARKER),
                         metaclasses.SETTER_NOARGS_MARKER)
        return

    def test_prop1_names(self):
        self.assertEqual(getattr(MyModel.get_prop1, 
                                 metaclasses.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop1",))

        self.assertEqual(getattr(MyModel.set_prop1, 
                                 metaclasses.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop1",))
        return

    def test_prop23_markers(self):
        self.assertEqual(getattr(MyModel.getter_for_props,
                                 metaclasses.GETTER_SETTER_ATTR_MARKER),
                         metaclasses.GETTER_ARGS_MARKER)

        self.assertEqual(getattr(MyModel.setter_for_prop2,
                                 metaclasses.GETTER_SETTER_ATTR_MARKER),
                         metaclasses.SETTER_ARGS_MARKER)

        self.assertEqual(getattr(MyModel.setter_for_prop3,
                                 metaclasses.GETTER_SETTER_ATTR_MARKER),
                         metaclasses.SETTER_ARGS_MARKER)
        return

    def test_prop23_names(self):
        self.assertEqual(getattr(MyModel.getter_for_props, 
                                 metaclasses.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop2","prop3"))

        self.assertEqual(getattr(MyModel.setter_for_prop2, 
                                 metaclasses.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop2",))

        self.assertEqual(getattr(MyModel.setter_for_prop3, 
                                 metaclasses.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop3",))
        return


if __name__ == "__main__":
    unittest.main()

