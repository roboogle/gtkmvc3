import _importer
from gtkmvc import Model, Controller, View
import gtk

class MyView (View):

    def __init__(self, ctrl):
        View.__init__(self, ctrl, "custom_wid.glade", "window1")
        return

    def create_my_custom_wid(self, str1, str2, int1, int2):
        st = "str1="+str1+" str2="+str2+"\nint1="+str(int1)+" int2="+str(int2)
        lb = gtk.Label(st)
        lb.show()
        return lb
    pass


m = Model()
c = Controller(m)
v = MyView(c)

gtk.main()
