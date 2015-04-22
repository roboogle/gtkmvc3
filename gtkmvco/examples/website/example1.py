import _importer, gtkmvc3, gtk
class MyModel (gtkmvc3.Model):
    name = "Roberto"
    age = 0
    __observables__ = ( "name", "age" ) 
    def show(self): print "MyModel: name=", self.name, "age=", self.age

class MyCtrl (gtkmvc3.Controller):    
    def on_button_clicked(self, button):
        self.model.show()
        return
    def on_window_delete_event(self, window, event):
        # quits the application
        gtk.main_quit()
        return True

m = MyModel()
v = gtkmvc3.View(glade="example1.glade")
c = MyCtrl(m, v, auto_adapt=True)
gtk.main() # run the application

