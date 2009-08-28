import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.basic import Adapter

import gtk

# This test uses only the tree rooted by 'window10'
class MyView (View):
    def __init__(self):
        View.__init__(self, "adapters.glade", "window10")
        return
    pass

import datetime
class MyModel (Model):
    file = "(please select a file)"
    __observables__ = ('file', )

    def __init__(self):
        Model.__init__(self)
        return
    pass


class MyCtrl (Controller):
    def __init__(self, m, v):
        Controller.__init__(self, m, v)
        return

    def register_view(self, v):
        v['window10'].connect('delete-event', self.on_delete_event)
        return
    
    def register_adapters(self):
        """Adapts both the File chooser button and the underneat label
        showing the file name"""
        self.adapt("file", "fcb_file")
        
        ad = Adapter(self.model, "file")
        ad.connect_widget(self.view["lbl_file"], setter=lambda w,v: \
                            w.set_markup("<b>%s</b>" % v))
        self.adapt(ad)
        return

    def on_delete_event(self, w, e):
        gtk.main_quit()
        return True
    
    pass

# ----------------------------------------------------------------------
# For [TW]:
# Sorry, this is necessarily tricky, and needs a better support to be
# integrated in future.
# This must be done *before* creating any controller using the added
# information for the adapter
from gtkmvc.adapters.default import __def_adapter
import types
__def_adapter.append(
    (gtk.FileChooserButton, "file-set",
     gtk.FileChooserButton.get_filename, gtk.FileChooserButton.set_filename,
     types.StringType))
# ----------------------------------------------------------------------


m = MyModel()
v = MyView()
c = MyCtrl(m, v)

gtk.main()



