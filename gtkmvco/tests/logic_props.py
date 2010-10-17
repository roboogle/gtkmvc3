"""
Test for getter and setter decorators, used in models to define 
logical properties
"""

import _importer
from gtkmvc import Model, getter, setter
from gtkmvc import model

import unittest

class MyModel (Model):

    @getter
    def get_prop1(self): return 0
    
    @setter
    def set_prop1(self, val): return

    @getter("prop2", "prop3")
    def getter_for_props(self, name): return name

    @setter("prop2")
    def setter_for_prop2(self, name, val): return

    @setter("prop3")
    def setter_for_prop3(self, name, val): return

    pass # end of class
# ----------------------------------------------------------------------

class LogicalProps(unittest.TestCase):
    def setUp(self): 
        return
        
    def test_prop1_markers(self):
        self.assertEqual(getattr(MyModel.get_prop1, 
                                 model.GETTER_SETTER_ATTR_MARKER),
                         model.GETTER_MARKER_VAL)

        self.assertEqual(getattr(MyModel.set_prop1, 
                                 model.GETTER_SETTER_ATTR_MARKER),
                         model.SETTER_MARKER_VAL)
        return

    def test_prop1_names(self):
        self.assertEqual(getattr(MyModel.get_prop1, 
                                 model.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop1",))

        self.assertEqual(getattr(MyModel.set_prop1, 
                                 model.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop1",))
        return

    def test_prop23_markers(self):
        self.assertEqual(getattr(MyModel.getter_for_props,
                                 model.GETTER_SETTER_ATTR_MARKER),
                         model.GETTER_MARKER_VAL)

        self.assertEqual(getattr(MyModel.setter_for_prop2,
                                 model.GETTER_SETTER_ATTR_MARKER),
                         model.SETTER_MARKER_VAL)

        self.assertEqual(getattr(MyModel.setter_for_prop3,
                                 model.GETTER_SETTER_ATTR_MARKER),
                         model.SETTER_MARKER_VAL)
        return

    def test_prop23_names(self):
        self.assertEqual(getattr(MyModel.getter_for_props, 
                                 model.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop2","prop3"))

        self.assertEqual(getattr(MyModel.setter_for_prop2, 
                                 model.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop2",))

        self.assertEqual(getattr(MyModel.setter_for_prop3, 
                                 model.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop3",))
        return


if __name__ == "__main__":
    unittest.main()

