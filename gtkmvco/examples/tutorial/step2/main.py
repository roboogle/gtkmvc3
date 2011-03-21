from model import MyModel
from ctrl import MyCtrl
from view import MyView
import gtk

# ----------------------------------------------------------------------
m = MyModel()
v = MyView()
c = MyCtrl(m, v)
# ----------------------------------------------------------------------

gtk.main()
