#  Author: Roberto Cavada <roboogle@gmail.com>
#  Modified by: Guillaume Libersat <glibersat AT linux62.org>
#
#  Copyright (c) 2005 by Roberto Cavada
#  Copyright (c) 2007 by Guillaume Libersat
#
#  pygtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc3 see <http://pygtkmvc3.sourceforge.net>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.

import itertools

from gtkmvc3.support.exceptions import ViewError

from gi.repository import Gtk
from gi.repository import GLib
# ----------------------------------------------------------------------


class View (object):
    top=None
    builder=None

    def __init__(self, top=None,
                 parent=None,
                 builder=None):
        """
        Only the first three may be given as positional arguments. If an
        argument is empty a class attribute of the same name is used. This
        does not work for *parent*.

        *top* is a string or a list of strings containing the names of our top
        level widgets. When using libglade only their children are loaded.
        This does NOT work with *builder*, each instance will create every
        window in the file.

        *parent* is used to call :meth:`set_parent_view`.

        *builder* is a path to an XML file defining widgets in GtkBuilder
        format. It can also be a :class:`Gtk.Builder` instance which already
        contains widgets. This is useful for internationalisation or if you
        want to break one XML file up into multiple views. Do not use that
        variant with class attributes, or all instances of this view will share
        one set of widgets.

        .. deprecated:: 1.99.1
           In future versions the functionality will be split into the new
           class :class:`ManualView` and its child :class:`BuilderView`.
        """
        self.manualWidgets = {}
        self.autoWidgets = {}
        self.__autoWidgets_calculated = False

        self.glade_xmlWidgets = []

        _top = top if top else self.top
        wids = ((_top,) if _top is None or isinstance(_top, str)
                else _top)  # Already a list or tuple

        # check if old 'glade' is still used
        if hasattr(self, "glade"):
            raise ViewError("View '%s' uses no longer "
                            "supported glade specification" % self.__class__)


        # retrieves objects from builder if available
        _builder = builder if builder else self.builder
        if _builder is not None:
            # if the user passed a Builder, use it as it is, otherwise
            # build one
            if isinstance(_builder, Gtk.Builder):
                self._builder = _builder
            else:
                self._builder = Gtk.Builder()
                self._builder.add_from_file(_builder)
        else:
            self._builder = None # no gtk builder

        # top widget list or singleton:
        if _top is not None:
            if len(wids) > 1:
                self.m_topWidget = []
                for i in range(0, len(wids)):
                    self.m_topWidget.append(self[wids[i]])
            else:
                self.m_topWidget = self[wids[0]]
        else:
            self.m_topWidget = None

        if parent is not None:
            self.set_parent_view(parent)

        self.builder_pending_callbacks = {}
        self.builder_connected = False

    def __getitem__(self, key):
        """
        Return the widget named *key* or raise KeyError.

        .. versionchanged:: 1.99.2
           Used to return None when the widget wasn't found.
        """
        wid = None

        # first try with manually-added widgets:
        if key in self.manualWidgets:
            wid = self.manualWidgets[key]

        if wid is None:
            # then try builder, starting from memoized
            if key in self.autoWidgets:
                wid = self.autoWidgets[key]
            else:
                # try with gtk.builder
                if wid is None and self._builder is not None:
                    wid = self._builder.get_object(key)
                    if wid is not None:
                        self.autoWidgets[key] = wid

        if not wid:
            raise KeyError(key)

        return wid

    def __setitem__(self, key, wid):
        """
        Add a widget. This overrides widgets of the same name that were loaded
        fom XML. It does not affect GTK container/child relations.

        If no top widget is known, this sets it.
        """
        self.manualWidgets[key] = wid
        if self.m_topWidget is None:
            self.m_topWidget = wid

    def show(self):
        """
        Call `show()` on each top widget or `show_all()` if only one is known.
        Otherwise does nothing.
        """
        top = self.get_top_widget()
        if isinstance(top, (list, tuple)):
            for t in top:
                if t is not None:
                    t.show()
        elif top is not None:
            top.show_all()

    def hide(self):
        """
        Call `hide_all()` on all known top widgets.
        """
        top = self.get_top_widget()
        if isinstance(top, (list, tuple)):
            for t in top:
                if t is not None:
                    t.hide_all()
        elif top is not None:
            top.hide_all()

    def get_top_widget(self):
        """
        Return a widget or list of widgets.
        """
        return self.m_topWidget

    def set_parent_view(self, parent_view):
        """
        Set ``self.``:meth:`get_top_widget` transient for
        ``parent_view.get_top_widget()``.
        """
        top = self.get_top_widget()
        if isinstance(top, (list, tuple)):
            for t in top:
                if t is not None:
                    t.set_transient_for(parent_view.get_top_widget())
        elif top is not None:
            top.set_transient_for(parent_view.get_top_widget())

    def set_transient(self, transient_view):
        """
        Set ``transient_view.get_top_widget()`` transient for
        ``self.``:meth:`get_top_widget`.
        """
        top = self.get_top_widget()
        if isinstance(top, (list, tuple)):
            for t in top:
                if t is not None:
                    transient_view.get_top_widget().set_transient_for(t)
        elif top is not None:
            transient_view.get_top_widget().set_transient_for(top)

    # Finds the right callback for custom widget creation and calls it
    # Returns None if an undefined or invalid  handler is found
    def _custom_widget_create(self, glade, function_name, widget_name,
                              str1, str2, int1, int2):
        # This code was kindly provided by Allan Douglas <zalguod at
        # users.sourceforge.net>
        if function_name is not None:
            handler = getattr(self, function_name, None)
            if handler is not None:
                return handler(str1, str2, int1, int2)

        return None

    def __builder_connect_pending_signals(self):
        """Called internally to actually make the internal Gtk.Builder
        instance connect all signals found in controllers controlling
        self."""
        class _MultiHandlersProxy (object):
            def __init__(self, funcs): self.funcs = funcs
            def __call__(self, *args, **kwargs):
                # according to gtk documentation, the return value of
                # a signal is the return value of the last executed
                # handler
                for func in self.funcs:
                    res = func(*args, **kwargs)
                return res

        final_dict = {n: (v.pop() if len(v) == 1
                          else _MultiHandlersProxy(v))
                      for n, v in self.builder_pending_callbacks.items()}

        self._builder.connect_signals(final_dict)

        self.builder_connected = True
        self.builder_pending_callbacks = {}

    def _builder_connect_signals(self, _dict):
        """Called by controllers which want to autoconnect their
        handlers with signals declared in internal Gtk.Builder.

        This method accumulates handlers, and books signal
        autoconnection later on the idle of the next occurring gtk
        loop. After the autoconnection is done, this method cannot be
        called anymore."""

        assert not self.builder_connected, "Gtk.Builder not already connected"

        if _dict and not self.builder_pending_callbacks:
            # this is the first call, book the builder connection for
            # later gtk loop
            GLib.idle_add(self.__builder_connect_pending_signals)

        for n, v in _dict.items():
            if n not in self.builder_pending_callbacks:
                _set = set()
                self.builder_pending_callbacks[n] = _set
            else:
                _set = self.builder_pending_callbacks[n]
            _set.add(v)

    def __iter__(self):
        """
        Yield names of widgets added with :meth:`__setitem__` and
        those loaded from XML.

        .. note::
           In case of name conflicts the result contains duplicates, but only
           the manually added widget is accessible via :meth:`__getitem__`.
        """
        # precalculates if needed
        self.__extract_autoWidgets()

        for i in itertools.chain(self.manualWidgets, self.autoWidgets):
            yield i

    def __extract_autoWidgets(self):
        """Extract autoWidgets map if needed, out of the glade
        specifications and gtk builder"""
        if self.__autoWidgets_calculated: return

        if self._builder is not None:
            for wid in self._builder.get_objects():
                # General workaround for issue
                # https://bugzilla.gnome.org/show_bug.cgi?id=607492
                try:
                    name = Gtk.Buildable.get_name(wid)
                except TypeError:
                    continue

                if name in self.autoWidgets and self.autoWidgets[name] != wid:
                    raise ViewError("Widget '%s' in builder also found in "
                        "glade specification" % name)

                self.autoWidgets[name] = wid

        self.__autowidgets_calculated = True
