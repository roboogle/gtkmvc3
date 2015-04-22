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
#  Please report bugs to <roboogle@gmail.com>.


from gtkmvc3.model import Model
from gtkmvc3.support import metaclasses
from gtkmvc3.support.porting import with_metaclass, add_metaclass

try: import threading as _threading
except ImportError: import dummy_threading as _threading

from gi.repository import Gtk
from gi.repository import GObject
GObject.threads_init()

from gi.repository import GLib


@add_metaclass(metaclasses.ObservablePropertyMetaMT)
class ModelMT (Model):
    """A base class for models whose observable properties can be
    changed by threads different than gtk main thread. Notification is
    performed by exploiting the gtk idle loop only if needed,
    otherwise the standard notification system (direct method call) is
    used. In this model, the observer is expected to run in the gtk
    main loop thread."""

    def __init__(self):
        Model.__init__(self)
        self.__observer_threads = {}
        self._prop_lock = _threading.Lock()

    def register_observer(self, observer):
        Model.register_observer(self, observer)
        self.__observer_threads[observer] = _threading.currentThread()

    def unregister_observer(self, observer):
        Model.unregister_observer(self, observer)
        del self.__observer_threads[observer]

    # ---------- Notifiers:

    def __notify_observer__(self, observer, method, *args, **kwargs):
        """This makes a call either through the gtk.idle list or a
        direct method call depending whether the caller's thread is
        different from the observer's thread"""

        assert observer in self.__observer_threads
        if _threading.currentThread() == self.__observer_threads[observer]:
            # standard call
            return Model.__notify_observer__(self, observer, method,
                                             *args, **kwargs)

        # multi-threading call
        GLib.idle_add(self.__idle_callback, observer, method, args, kwargs)

    def __idle_callback(self, observer, method, args, kwargs):
        method(*args, **kwargs)
        return False


# ----------------------------------------------------------------------
class TreeStoreModelMT (with_metaclass(
        metaclasses.ObservablePropertyGObjectMetaMT,
        ModelMT, Gtk.TreeStore)):
    """Use this class as base class for your model derived by
    Gtk.TreeStore"""

    def __init__(self, column_type, *args):
        ModelMT.__init__(self)
        Gtk.TreeStore.__init__(self, column_type, *args)


# ----------------------------------------------------------------------
class ListStoreModelMT (with_metaclass(
        metaclasses.ObservablePropertyGObjectMetaMT,
        ModelMT, Gtk.ListStore)):
    """Use this class as base class for your model derived by
    Gtk.ListStore"""

    def __init__(self, column_type, *args):
        ModelMT.__init__(self)
        Gtk.ListStore.__init__(self, column_type, *args)


# ----------------------------------------------------------------------
class TextBufferModelMT (with_metaclass(
        metaclasses.ObservablePropertyGObjectMetaMT,
        ModelMT, Gtk.TextBuffer)):
    """Use this class as base class for your model derived by
    Gtk.TextBuffer"""

    def __init__(self, table=None):
        ModelMT.__init__(self)
        Gtk.TextBuffer.__init__(self, table)
