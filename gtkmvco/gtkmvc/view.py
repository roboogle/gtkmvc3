#  Author: Roberto Cavada <cavada@fbk.eu>
#  Modified by: Guillaume Libersat <glibersat AT linux62.org>
#
#  Copyright (c) 2005 by Roberto Cavada
#  Copyright (c) 2007 by Guillaume Libersat
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
#  or email to the author Roberto Cavada <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.

from gtkmvc.support.log import logger

try:
    import gtk.glade
    __glade_is_available__ = True
except ImportError: __glade_is_available = False

try:
    from gtk import Builder
    __builder_is_available__ = True
except ImportError: __builder_is_available__ = False

# verbose message
if not __glade_is_available__ or not __builder_is_available__:
    logger.warn({(False, False) : "both glade and gtk.Builder are not available: relying only on manual widgets in views",
              (False, True) : "gtk.Builder is not available, relying on manual and glade based views only", 
              (True, False) : "glade is not available, relying on manual and gtk.Builder based views only", 
}[(__builder_is_available__, __glade_is_available__)])
    pass
    
import types
# ----------------------------------------------------------------------

class View (object):
    glade = None
    top=None
    builder=None
    
    def __init__(self, glade=None, top=None,
                 builder=None,
                 parent=None, 
                 controller=None):
        """If glade filename is not given (or None) next parameter top
        must be not given neither (or None). builder can be a filename
        for gtk.Builder, or an instance of a gtk.Builder.  If glade
        and builder are both None or not given, widgets must be
        connected manually. top can be either a string name or list of
        names, representing the name of the top level widget, or a
        list of names of top level widgets in the glade file. Notice
        that until gtk.Builder will not support method
        add_objects_from_file, top can be used only when glade is
        specified. parent is another View instance used to create a
        hierarchy of views. If controller is passed, then self will
        register itself within it. This is provided for backward
        compatibility when controllers had to be created before views
        (DO NOT USE IN NEW CODE)."""

        self.manualWidgets = {}
        self.autoWidgets = {}
        self.__autoWidgets_calculated = False
        
        self.glade_xmlWidgets = []
        
        # Sets a callback for custom widgets
        if __glade_is_available__:
            gtk.glade.set_custom_handler(self._custom_widget_create)
            pass

        if top: _top = top
        else: _top = self.top
        if type(_top) == types.StringType or _top is None:
            wids = (_top,)
        else: wids = _top  # Already a list or tuple

        # retrieves XML objects from glade
        if glade: _glade = glade
        else: _glade = self.glade

        if _glade is not None:
            if not __glade_is_available__:
                logger.critical("Module gtk.glade was required, by not available")
                sys.exit(1)
                pass
            for wid in wids:
                self.glade_xmlWidgets.append(gtk.glade.XML(_glade, wid))
                pass
            pass

        # retrieves objects from builder if available
        if builder: _builder = builder
        else: _builder = self.builder
        if _builder is not None:
            if not __builder_is_available__:
                log.critical("gtk.Builder was required, by not available")
                sys.exit(1)
                pass
            # if the user passed a Builder, use it as it is, otherwise
            # build one
            if isinstance(_builder, gtk.Builder):
                self._builder = _builder
            else:
                self._builder = gtk.Builder()
                self._builder.add_from_file(_builder)
                pass
            pass
        else: self._builder = None # no gtk builder
            
        # top widget list or singleton:
        if _top is not None:
            if len(wids) > 1:
                self.m_topWidget = []
                for i in range(0, len(wids)):
                    self.m_topWidget.append(self[wids[i]])
                    pass
            else: self.m_topWidget = self[wids[0]]
        else:  self.m_topWidget = None
       
        if parent is not None: self.set_parent_view(parent)

        if controller: 
            # this is deprecated
            import warnings
            warnings.warn("Controller specified in View constructor is no longer expected",
                          DeprecationWarning)
            import gobject
            gobject.idle_add(controller._register_view, self)
            pass

        return
       
    # Gives us the ability to do: view['widget_name'].action()
    # Returns None if no widget name has been found.
    def __getitem__(self, key):
        wid = None

        # first try with manually-added widgets:
        if self.manualWidgets.has_key(key):
            wid = self.manualWidgets[key]
            pass
        pass
        
        if wid is None:
            # then try with glade and builder, starting from memoized 
            if self.autoWidgets.has_key(key): wid = self.autoWidgets[key]
            else:
                # try with glade
                for xml in self.glade_xmlWidgets:
                    wid = xml.get_widget(key)
                    if wid is not None:
                        self.autoWidgets[wid.get_name()] = wid
                        break
                    pass

                # try with gtk.builder                
                if wid is None and self._builder is not None:
                    wid = self._builder.get_object(key)
                    if wid is not None:
                        self.autoWidgets[wid.get_name()] = wid
                        pass
                    pass                            
                pass
            pass
        
        return wid
    
    # You can also add a single widget:
    def __setitem__(self, key, wid):
        self.manualWidgets[key] = wid
        if (self.m_topWidget is None): self.m_topWidget = wid
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

    # Finds the right callback for custom widget creation and calls it
    # Returns None if an undefined or invalid  handler is found
    def _custom_widget_create(self, glade, function_name, widget_name,
                              str1, str2, int1, int2):
        # This code was kindly provided by Allan Douglas <zalguod at
        # users.sourceforge.net>
        if function_name is not None:
            handler = getattr(self, function_name, None)
            if handler is not None: return handler(str1, str2, int1, int2)
            pass        
        return None

    # implements the iteration protocol
    def __iter__(self):
        # precalculates if needed
        self.__extract_autoWidgets()

        import itertools
        for i in itertools.chain(self.manualWidgets, self.autoWidgets): yield i
        return

    def __extract_autoWidgets(self):
        """Extract autoWidgets map if needed, out of the glade
        specifications and gtk builder"""
        if self.__autoWidgets_calculated: return

        if __glade_is_available__:
            for xml in self.glade_xmlWidgets:
                for wid in xml.get_widget_prefix(""):
                    wname = gtk.glade.get_widget_name(wid)
                    if wname not in self.autoWidgets:
                        self.autoWidgets[wname] = wid
                        pass                    
                    pass
                pass
            pass

        if self._builder is not None:
            for wid in self._builder.get_objects():
                name = wid.get_name()
                if name in self.autoWidgets and self.autoWidgets[name] != wid:
                    log.error("Widget '%s' in builder also found in glade specification" % name)
                    sys.exit(1)
                    pass
                self.autoWidgets[name] = wid
                pass
            pass
        
        self.__autowidgets_calculated = True
        return
    
    pass # end of class View
