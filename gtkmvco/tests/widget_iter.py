"""
Tests using more than one concurrent iter on a view.
"""
import _importer

import gtk
import gtkmvc

class View(gtkmvc.View):
    glade = "adapters.glade"
    top = "window7"

class Ctrl(gtkmvc.Controller):

    def register_view(self, view):
        iter1 = iter(view)
        iter2 = iter(view)
        set1 = set()
        set2 = set()
        try:
            for item1 in iter1:
                item2 = iter2.next()
                set1.add(item1)
                set2.add(item2)
            assert set1 == set2
            print "OK"
        except (StopIteration, AssertionError):
            print "Failed"
        gtk.main_quit()

    def on_button7_clicked(self, button):
        pass
    
m = gtkmvc.Model()
v = View()
c = Ctrl(m, v)

gtk.main()
