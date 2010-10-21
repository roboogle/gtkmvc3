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

    _value = 0

    @Model.getter
    def get_prop1(self): return self._value
    
    @Model.setter
    def set_prop1(self, val): self._value = val

    @Model.getter("prop2", "prop3")
    def getter_for_props(self, name): return name

    @Model.setter("prop2")
    def setter_for_prop2(self, name, val): return

    @Model.setter("prop3")
    def setter_for_prop3(self, name, val): return

    pass # end of class
# ----------------------------------------------------------------------


# this class checks that hierarchies are not broken
class MyModel2 (MyModel):
    
    __observables__ = ("prop4",)

    # this is used to check overriding in derivated classes
    def get_prop1(self): return 1
    
    @Model.setter
    def set_prop4(self, val): return

    @Model.getter("*")
    def getter_for_all_props(self, name): return name
    pass


class LogicalProps(unittest.TestCase):
    def setUp(self): 
        return
        
    def test_prop1_markers(self):
        # checks that getter/setter decorator correctly mark methods
        self.assertEqual(getattr(MyModel.get_prop1, 
                                 metaclasses.GETTER_SETTER_ATTR_MARKER),
                         metaclasses.GETTER_NOARGS_MARKER)

        self.assertEqual(getattr(MyModel.set_prop1, 
                                 metaclasses.GETTER_SETTER_ATTR_MARKER),
                         metaclasses.SETTER_NOARGS_MARKER)
        return

    def test_prop1_names(self):
        # checks that getter/setter decorator correctly mark methods
        self.assertEqual(getattr(MyModel.get_prop1, 
                                 metaclasses.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop1",))

        self.assertEqual(getattr(MyModel.set_prop1, 
                                 metaclasses.GETTER_SETTER_ATTR_PROP_NAMES),
                                 ("prop1",))
        return

    def test_prop23_markers(self):
        # checks that getter/setter decorator correctly mark methods
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
        # checks that getter/setter decorator correctly mark methods
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

    def test_prop_base_rw(self):
        # test read/write in base
        m = MyModel()
        m.prop1 = 10
        self.assertEqual(m.prop1, 10)
        return

    def test_prop_der_rw(self):
        # test read/write in derivated
        m = MyModel2()
        m.prop1 = 10
        self.assertEqual(m._value, 10)
        return

    def test_prop_der_overriding(self):
        # tests getter overriding works
        m = MyModel2()
        m.prop1 = 10
        self.assertEqual(m.prop1, 1)
        return
        
    # tests that derivated properties are handled
    def test_prop_der_local(self):
        m = MyModel2()
        m.prop4 = "ciao" # setters is dummy
        self.assertEqual(m.prop4, "prop4")
        return
    pass


if __name__ == "__main__":
    unittest.main()
