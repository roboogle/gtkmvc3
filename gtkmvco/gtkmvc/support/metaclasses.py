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

from metaclass_base import PropertyMeta
import types


class ObservablePropertyMeta (PropertyMeta):
    """Classes instantiated by this meta-class must provide a method named
    notify_property_change(self, prop_name, old, new)"""
    def __init__(cls, name, bases, dict):
        PropertyMeta.__init__(cls, name, bases, dict)
        return    
    
    def get_setter_source(cls, setter_name, prop_name):
        return """def %(setter)s(self, val): 
 old = self._prop_%(prop)s 
 self._prop_%(prop)s = type(self).create_value('%(prop)s', val, self)
 if type(old) != type(self._prop_%(prop)s): self._reset_property_notification('%(prop)s')
 self.notify_property_value_change('%(prop)s', old, val)
 return
""" % {'setter':setter_name, 'prop':prop_name}

    pass #end of class



try:
    from gobject import GObjectMeta
    class ObservablePropertyGObjectMeta (ObservablePropertyMeta, GObjectMeta): pass
except:
    class ObservablePropertyGObjectMeta (ObservablePropertyMeta): pass
    pass


