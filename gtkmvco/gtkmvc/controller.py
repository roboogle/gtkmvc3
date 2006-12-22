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


from gtkmvc.observer import Observer

class Controller (Observer):
    """We put all of our gtk signal handlers into a class.  This lets us bind
    all of them at once, because their names are in the class dict.
    This class automatically register its instances as observers into the
    corresponding model.
    Also, when a view is created, the view calls method register_view,
    which can be oveloaded in order to connect signals and perform other
    specific operation"""

    def __init__(self, model):
        Observer.__init__(self, model)

        self.view = None
        return

    def register_view(self, view):
        assert(self.view is None)
        self.view = view
        return

    pass # end of class Controller
