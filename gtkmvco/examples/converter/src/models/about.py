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
#  or email to the author <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


import utils._importer
import utils.globals

from gtkmvc import Model
import os.path


class AboutModel (Model):
    """An almost empty model for the 'About' dialog. It has been added
    to show how models might be used to separate the logics. In the
    spirit of this tutorial, the usage of an observable property for
    the credits text is an exaggeration.""" 

    credits = ""
    CREDITS_FILE = os.path.join(utils.globals.TOP_DIR, "about")

    __observables__ = ("credits",)
    
    def __init__(self):
        Model.__init__(self)

        self.credits = open(self.CREDITS_FILE, "r").read()
        return

    pass # end of class
# ----------------------------------------------------------------------

