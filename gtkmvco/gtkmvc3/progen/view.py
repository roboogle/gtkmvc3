#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2007-2015 by Roberto Cavada
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

from gtkmvc3 import View
from gtkmvc3.progen.globals import PROGEN_DIR
assert PROGEN_DIR # Must be found!
import os

class ProgenView (View):
    builder = os.path.join(PROGEN_DIR, "progen.ui")

    def __init__(self):
        super(ProgenView, self).__init__()
        self.setup_widgets()

    def setup_widgets(self):
        self['notebook_appl'].set_show_tabs(False)
        nb = self['notebook']
        nb.set_show_tabs(False)
        self['button_prev'].set_sensitive(False)

    def next_page(self):
        self.__inc_page(1)

    def prev_page(self):
        self.__inc_page(-1)

    def __inc_page(self, inc):
        nb = self['notebook']
        page = nb.get_current_page()
        pages = nb.get_n_pages()

        npage = page + inc
        self['button_prev'].set_sensitive(npage > 0)
        if npage >= 0:
            self['button_next'].set_sensitive(npage < pages-1)
            if npage < pages:
                nb.set_current_page(npage)
