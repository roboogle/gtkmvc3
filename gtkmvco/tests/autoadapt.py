"""
Test should show two entries and a button. Pressing it should print both
values.
"""

import _importer, gtkmvc

class MyModel (gtkmvc.Model):
    name = "Roberto"
    age = 0
    __observables__ = ( "name", "age" )

    def show(self): print "MyModel: name=", self.name, "age=", self.age    
    pass # end of class

# MyView.py
import gtkmvc
import gtk
class MyView (gtkmvc.View):

    def __init__(self):
        gtkmvc.View.__init__(self)
        self.setup_widgets()
        return
    
    def setup_widgets(self):
        self['window'] = gtk.Window()
        self['window'].set_title("A damned small example")
        t = gtk.Table(rows=2, columns=2)
        t.set_row_spacings(12)
        t.set_col_spacings(6)

        t.attach(gtk.Label("Name:"), 0, 1, 0, 1)
        t.attach(gtk.Label("Age:"), 0, 1, 1, 2)

        self['entry_name'] = gtk.Entry()
        t.attach(self['entry_name'], 1, 2, 0, 1)
        self['sb_age'] = gtk.SpinButton(gtk.Adjustment(lower=0, upper=100,
                                                       step_incr=1))
        t.attach(self['sb_age'], 1, 2, 1, 2)

        self['button'] = gtk.Button("Click me!")
        h = gtk.VBox()
        h.set_spacing(12)
        h.pack_start(t); h.pack_start(self['button'])
        
        self['window'].add(h)
        self['window'].show_all()
        return
    pass # end of class

# MyCtrl.py
import gtkmvc
import gtk
class MyCtrl (gtkmvc.Controller):
    def register_view(self, view):
        super(MyCtrl, self).register_view(view)
        view['window'].connect('delete-event', self.on_window_delete_event)
        view['button'].connect('clicked', self.on_button_clicked)
        return

    def register_adapters(self):
        # only name will be autoadapted
        self.adapt("age")        
        return
    
    def on_button_clicked(self, button):
        self.model.show()
        return

    def on_window_delete_event(self, window, event):
        # quits the application
        gtk.main_quit()
        return True    
    pass # end of class


# main.py
m = MyModel()
v = MyView()
c = MyCtrl(m, v, auto_adapt=True)

gtk.main()
