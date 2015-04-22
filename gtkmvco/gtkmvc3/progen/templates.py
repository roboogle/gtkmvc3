## This file contains the default templates used when creating a
## project
# >>>   IMPORTANT!  <<<<
# Notice that default license is GPL

__all__ = ( "DEFAULT_HEADER", "DEFAULT_MAP" )

import gtkmvc3

header = """#  -------------------------------------------------------------------------
#  This file was initially generated by gtkmvc3 progen-$version
#  Generation timestamp: $date
#  -------------------------------------------------------------------------
#
#  Author: $author  $email
#
#  $copyright
#
#  This file is part of ${name}.
#
$license
#  -------------------------------------------------------------------------

$comment
"""


gpl = """#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
"""

model = """
from gtkmvc3 import ${base_class_name}

class ${class_name} (${base_class_name}):

    # Observable properties
    somevalue = 0
    __observables__ = ("somevalue",)

    def __init__(self):
        ${base_class_name}.__init__(self)
        return

    pass # end of class ${class_name}
"""

ctrl = """
from gtkmvc3 import Controller
from gtkmvc3 import adapters
from gi.repository import Gtk

class ${class_name} (${base_class_name}):

    def __init__(self, model, view):
        ${base_class_name}.__init__(self, model, view)
        return

    def register_view(self, view):
        # setup of widgets
        self.view['${top_widget}'].connect('delete-event', self.on_${top_widget}_delete_event)
        return

    def register_adapters(self):
        # setup of adapters
        return

    # ---------------------------------------------------------------
    #        Signal handlers
    # ---------------------------------------------------------------
    def on_${top_widget}_delete_event(self, win, event):
        Gtk.main_quit() # say goodbye
        return True

    # ---------------------------------------------------------------
    #        Notifications from observable properties
    # ---------------------------------------------------------------

    # For value-change notifications
#     @Controller.observe("<property_name_here>", assign=True)
#     def value_change(self, model, prop_name, info):
#         # info contains 'new' and 'old' values
#         return

    # For value-change of containers like lists, maps, or method calls for observable class instances.
    # There exist 'before' and 'after' versions, you can use both or only one, depending on your need.
#     @Controller.observe("<property_name_here>", before=True, after=True)
#     def method_call(self, model, prop_name, info):
#         # Info contains:
#         # 'instance' is the object that is being changed (the list for example)
#         # 'method_name' is the name of the method that is used to change it ('append' for example)
#         # 'args' is the list of arguments of the invoked method 'name'
#         # 'kwargs' is the keywords map of the invoked method 'name'
#         # 'result' (only for 'after' notifications) the value returned by the method after the call
#         return
#

    @Controller.observe("somevalue", assign=True)
    def somevalue_change(self, model, prop_name, info):
        return

    pass # end of class ${class_name}
"""

view_builder = """
from gtkmvc3 import View
import utils.globals

from gi.repository import Gtk
import os.path

class ${class_name} (${base_class_name}):
    builder = os.path.join(utils.globals.UI_DIR, "builder", "${builder_fn}")
    top = "${top_widget}"
    def __init__(self):
        ${base_class_name}.__init__(self)

        # construction of manual widgets and other settings
        return

    pass # end of class ${class_name}
"""


view_nobuilder = """
from gtkmvc3 import View
from gi.repository import Gtk

class ${class_name} (${base_class_name}):

    def __init__(self):
        ${base_class_name}.__init__(self)

        # construction of manual widgets and other settings
        w = Gtk.Window()
        w.set_title("Hello ${name}")
        h = Gtk.VBox(); w.add(h)
        lbl = Gtk.Label()
        lbl.set_markup("<big><b>Hello ${author}!</b></big>")
        h.add(lbl)
        self['label1'] = lbl

        lbl = Gtk.Label()
        lbl.set_markup('''This is a demo of a <b>gtkmvc3</b>-based application
without a <i>builder</i> file''')
        h.add(lbl)
        self['label2'] = lbl

        w.show_all()
        self['${top_widget}'] = w
        return

    pass # end of class ${class_name}
"""

glob = """
import os.path
import sys

if sys.argv[0]: top_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
else: top_dir = "."

# ----------------------------------------------------------------------
TOPDIR = top_dir
RESOURCES_DIR = os.path.join(TOPDIR, "${res_name}")
UI_DIR = os.path.join(RESOURCES_DIR, "ui")
STYLES_DIR = os.path.join(RESOURCES_DIR, "styles")
APPL_SHORT_NAME = "${name}"
APPL_VERSION = (1, 0, 0)
# ----------------------------------------------------------------------

"""


main = '''
from gi.repository import Gtk


def setup_path():
    """Sets up the python include paths to include needed directories"""
    import os.path; import sys
    from ${src_name}.utils.globals import TOPDIR
    sys.path.insert(0, os.path.join(TOPDIR, "${res_name}", "external"))
    sys.path.insert(0, os.path.join(TOPDIR, "${src_name}"))


def check_requirements():
    """Checks versions and other requirements"""
    import gtkmvc3;
    gtkmvc3.require("1.99.1")


def main(*args, **kargs):
    ${model_import} as ApplModel
    ${ctrl_import} as ApplCtrl
    ${view_import} as ApplView

    m = ApplModel()
    v = ApplView()
    c = ApplCtrl(m, v)

    Gtk.main()


if __name__ == "__main__":
    setup_path()
    check_requirements()
    main()
'''

builder_file = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.18.3 -->
<interface>
  <requires lib="gtk+" version="3.0"/>
  <object class="GtkWindow" id="${top_widget}">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
    <property name="border_width">12</property>
    <property name="title" translatable="yes">Hello ${name}</property>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
        <property name="spacing">12</property>
        <child>
          <object class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
            <property name="label" translatable="yes">&lt;big&gt;&lt;b&gt;Hello ${author}!&lt;/b&gt;&lt;/big&gt;

This is a demo from gtkmvc3 Project Generator</property>
            <property name="use_markup">True</property>
            <property name="justify">center</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="label2">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="events">GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK</property>
            <property name="label" translatable="yes">To start editing your project:
1. Change Gtk.Builder file into resources/ui by using &lt;tt&gt;Glade&lt;/tt&gt;
2. Adapt skeleton source code that has been generated

Hope you will enjoy designing and developing with gtkmvc3!

For further information take a tour at
&lt;u&gt;https://github.com/roboogle/gtkmvc3&lt;/u&gt;</property>
            <property name="use_markup">True</property>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
'''

# These are exported outside
# ----------------------------------------------------------------------
DEFAULT_HEADER = header
VERSION = list(map(str, gtkmvc3.get_version()))
DEFAULT_MAP = {'license': gpl, 'version': ".".join(VERSION) }
# ----------------------------------------------------------------------