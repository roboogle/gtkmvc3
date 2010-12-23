#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (c) 2006 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


from gtkmvc import Controller
class MyController (Controller):
    
    def register_view(self, view):
        readme = open("README","r").read()
        view.set_info(readme)
        view.set_label("Hello")
        return

    # gtk signals
    def on_button_clicked(self, button): self.model.run_test()

    def on_window_delete_event(self, window, event):
        import gtk
        gtk.main_quit()
        return True
    
    # observd properties
    @Controller.observe("counter", assign=True)
    def counter_change(self, model, prop_name, info):
        self.view.set_label("%d" % info.new)
        return

    @Controller.observe("busy", assign=True)
    def busy_change(self, model, prop_name, info):
        if info.new != info.old:
            self.view['button'].set_sensitive(not info.new)
            if not info.new: self.view['button'].grab_focus()
        return

    pass # end of class

