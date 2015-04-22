#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2007-2015 by Roberto Cavada
#
#  gtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  gtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#  02111-1307 USA.
#
#  For more information on gtkmvc3 see
#  <https://github.com/roboogle/gtkmvc3> or email to the author Roberto
#  Cavada <roboogle@gmail.com>.  Please report bugs to
#  <roboogle@gmail.com>.



# A simple demo showing an Adapter at work
# A text entry is kept aligned with an observable property
# With respect to simple.py, when button is pressed the model is
# changed, and the entry widget got updated accordingly.

import _importer

import gtkmvc3
import gtk

# hand-made view simply containing a text entry and a button
class MyView (gtkmvc3.View):
    def __init__(self):
        super(MyView,self).__init__()

        w = gtk.Window()
        e = gtk.Entry()
        b = gtk.Button("Press")

        h = gtk.VBox(); h.add(e); h.add(b)
        w.add(h)
        w.show_all()
        self['entry_text'] = e
        self['button'] = b
        self['window'] = w
        return
    pass # end of class
 #-----------------------------------------------------------

# The controller. Boring code now is handled by adapters!
class MyCtrl (gtkmvc3.Controller):

    def register_adapters(self):
        # good time to create adapters
        self.adapt("text")
        return

    def register_view(self, view):
        view['button'].connect('clicked', self.on_button_clicked)
        view['window'].connect('delete-event', gtk.main_quit)
        return

    # signal handlers
    def on_button_clicked(self, button):
        print "Text is:'%s'" % self.model.text
        self.model.text = "Clicking the button changes the model as well!"
        return

    pass # end of class
 #-----------------------------------------------------------

class MyModel (gtkmvc3.Model):
    text = "Ciao"
    __observables__ = ("text",)
    pass # end of class
 #-----------------------------------------------------------

m = MyModel()
v = MyView()
c = MyCtrl(m, v)

gtk.main()
