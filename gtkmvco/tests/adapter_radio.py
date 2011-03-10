import _importer
from gtkmvc import Model, View, Controller
import gtk

# Shows how a group of radio buttons or actions can be adapted to a
# unique OP. The string value of the OP is the label of the
# buttons/actions. The setting is bi-directional, but to set the
# active radio the exacct match is required, or the radio is not set.

class MyModel (Model):

    value = "Value2"
    __observables__ = ("value",)
    pass

class MyViewButtons (View):
    builder = "adapter_radio_buttons.glade"
    top = "window1"
    pass

class MyViewActions (View):
    builder = "adapter_radio_actions.glade"
    top = "window1"

    def __init__(self):
        View.__init__(self)

        # sets the rb active state
        self["rb1"].set_active(True)
        for name in "rb2 rb3 rb4".split(): self[name].set_active(False)
        return
    pass

class MyCtrl (Controller):

    def register_view(self, view):
        view['window1'].connect("delete-event", lambda x,e: gtk.main_quit())
        return
    
    def register_adapters(self):
        self.adapt("value", "rb1")
        self.adapt("value", "rb2")
        self.adapt("value", "rb3")
        self.adapt("value", "rb4")

        # this is used to show the current value
        self.adapt("value", "entry_value")
        return

    pass

m = MyModel()

# enable these to use radio buttons:
v1 = MyViewButtons() 
c1 = MyCtrl(m, v1)

# enable these to use radio actions:
v2 = MyViewActions() 
c2 = MyCtrl(m, v2)

gtk.main()

