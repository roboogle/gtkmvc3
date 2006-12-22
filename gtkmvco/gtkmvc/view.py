#  Author: Roberto Cavada <cavada@irst.itc.it>
#
#  Copyright (c) 2005 by Roberto Cavada
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
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <cavada@irst.itc.it>.
#  Please report bugs to <cavada@irst.itc.it>.


import gtk.glade
from controller import Controller
import types

class View (object):

    def __init__(self, controller, glade_filename=None,
                 glade_top_widget_name=None, parent_view=None, register=True):
        """If register is False you *must* call 'controller.register_view(self)'
        from the derived class constructor (i.e. registration is delayed)
        If filename is not given (or None) all following parameters must be
        not given (or None). In that case widgets must be connected manually.
        glade_top_widget_name can be either a string name or list of names."""
        self.manualWidgets = {}
        self.xmlWidgets = []

        if (( type(glade_top_widget_name) == types.StringType)
            or (glade_top_widget_name is None) ):
            wids = (glade_top_widget_name,)
        else: wids = glade_top_widget_name  # Already a list or tuple

        if (glade_filename is not None):
            for i in range(0,len(wids)):
                self.xmlWidgets.append(gtk.glade.XML(glade_filename, wids[i]))
                pass
            pass

        # top widget list or singleton:
        if (glade_top_widget_name is not None):
            if len(wids) > 1:
                self.m_topWidget = []
                for i in range(0, len(wids)):
                    self.m_topWidget.append(self[wids[i]])
                    pass
            else: self.m_topWidget = self[wids[0]]
        else:  self.m_topWidget = None

        if (glade_filename is not None): self.autoconnect_signals(controller)
        if (register):                   controller.register_view(self)
        if (not parent_view is None):    self.set_parent_view(parent_view)
        return

    # Gives us the ability to do: view['widget_name'].action()
    # Returns None if no widget name has been found.
    def __getitem__(self, key):
        wid = None
        for xml in self.xmlWidgets:
            wid = xml.get_widget(key)
            if wid is not None: break
            pass
        
        if (wid is None):
            # try with manually-added widgets:
            if (self.manualWidgets.has_key(key)):
                wid = self.manualWidgets[key]
                pass
            pass
        return wid
    
    # You can also add a single widget:
    def __setitem__(self, key, wid):
        self.manualWidgets[key] = wid
        if (self.m_topWidget is None): self.m_topWidget = wid
        return

    # performs Controller's signals auto-connection:
    def autoconnect_signals(self, controller):
        dict = {}
        member_names = dir(controller)
        for name in member_names:
            method = getattr(controller, name)
            if (not callable(method)): continue
            assert(not dict.has_key(name)) # not already connected!
            dict[name] = method
            pass

        for xml in self.xmlWidgets: xml.signal_autoconnect(dict) 
        return

    def show(self):
        ret = True
        top = self.get_top_widget()
        if type(top) in (types.ListType, types.TupleType):
            for t in top:
                if t is not None: ret = ret and t.show()
                pass
        elif (top is not None): ret = top.show_all()
        else:                   ret = False
        return ret
        
        
    def hide(self):
        top = self.get_top_widget()
        if type(top) in (types.ListType, types.TupleType):
            for t in top:
                if t is not None: t.hide_all()
                pass
        elif top is not None: top.hide_all()
        return

    # Returns the top-level widget, or a list of top widgets
    def get_top_widget(self):
        return self.m_topWidget


    # Set parent view:
    def set_parent_view(self, parent_view):
        top = self.get_top_widget()
        if type(top) in (types.ListType, types.TupleType):
            for t in top:
                if t is not None:
                    t.set_transient_for(parent_view.get_top_widget())
                    pass
                pass
        elif (top is not None):
            top.set_transient_for(parent_view.get_top_widget())
            pass
        
        return

    # Set the transient for the view:
    def set_transient(self, transient_view):
        top = self.get_top_widget()
        if type(top) in (types.ListType, types.TupleType):
            for t in top:
                if t is not None:
                    transient_view.get_top_widget().set_transient_for(t)
                    pass
                pass
        elif (top is not None):
            transient_view.get_top_widget().set_transient_for(top)
            pass
        return

    pass # end of class View
