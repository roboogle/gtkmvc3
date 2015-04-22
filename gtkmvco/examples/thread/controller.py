#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2006-2015 by Roberto Cavada
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
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.


from gi.repository import Gtk

from gtkmvc3 import Controller


class MyController (Controller):
    def register_view(self, view):
        readme = open("README","r").read()
        view.set_info(readme)
        view.set_label("Hello")

    # gtk signals
    def on_button_clicked(self, button):
        self.model.run_test()

    def on_window_delete_event(self, window, event):
        from gi.repository import Gtk
        Gtk.main_quit()
        return True

    # observed properties
    @Controller.observe("counter", assign=True)
    def counter_change(self, model, prop_name, info):
        self.view.set_label("%d" % info.new)

    @Controller.observe("busy", assign=True)
    def busy_change(self, model, prop_name, info):
        if info.new != info.old:
            self.view['button'].set_sensitive(not info.new)
            if not info.new:
                self.view['button'].grab_focus()

    pass # end of class
