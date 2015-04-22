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
#  or email to the author <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.


def setup_path():
    """Sets up the python include paths to include src"""
    import os.path; import sys

    if sys.argv[0]:
        top_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        sys.path = [os.path.join(top_dir, "src")] + sys.path
        pass
    return


def main():
    setup_path()

    from models.application import ApplicationModel as MyModel
    from controllers.application import ApplicationCtrl as MyCtrl
    from views.application import ApplicationView as MyView

    import gtk
    
    m = MyModel()
    v = MyView()
    c = MyCtrl(m, v)

    gtk.main()
    return

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
    pass


