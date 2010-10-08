"""
Test should show two labels, "Test" and "str1=str1...".
"""
import _importer
from gtkmvc import Model, Controller, View
import gtk

class MyView (View):

    glade = "custom_wid.glade"
    top = "window1"

    def create_my_custom_wid(self, str1, str2, int1, int2):
        st = "str1="+str1+" str2="+str2+"\nint1="+str(int1)+" int2="+str(int2)
        lb = gtk.Label(st)
        lb.show()
        return lb
    pass


m = Model()
v = MyView()
c = Controller(m, v)

gtk.main()
