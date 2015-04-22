import os.path
import _importer # this is an helper to import gtkmvc3
from gtkmvc3 import View

GLADE_PATH = "./"

class ExampleView (View):
    """The application view. Contains only the main window1 tree."""
    builder = os.path.join(GLADE_PATH, "example.glade")
    top = "window1"

    def set_msg(self, msg):
       self['label_text'].set_text(msg)
       self['label_text_len'].set_text(str(len(msg)))
       return

    pass # end of class
