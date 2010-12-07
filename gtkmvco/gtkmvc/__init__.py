#  Author: Roberto Cavada <roboogle@gmail.com>
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
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


__all__ = ["Model", "TreeStoreModel", "ListStoreModel", "TextBufferModel", 
           "ModelMT",
           "Controller", "View", "Observer",
           "Observable",
           "observable", "observer", "adapters", # packages
           ]

__version = (1,99,1)

# visible classes
from model import Model, TreeStoreModel, ListStoreModel, TextBufferModel
from model_mt import ModelMT
from controller import Controller
from view import View
from observer import Observer
from observable import Observable

# visible modules
import observable, observer, adapters

def get_version(): return __version

def require(request):
    """
    Raise :exc:`AssertionError` is gtkmvc version is not compatible.
    
    *request* a dotted string or iterable of string or integers representing the
    minimum version you need. ::
    
     require("1.0")
     require(("1", "2", "2"))
     require([1,99,0])
    """
    try:
        request = request.split(".")
    except AttributeError:
        pass
    request = map(int, request)

    provide = list(__version)

    if request[0] != 1:
        raise ValueError("gtkmvc %s is not a valid version" % request)
    if request[1] < 3:
        raise AssertionError("gtkmvc %s is very different from %s" % (
            provide, request))
    if request > provide:
        raise AssertionError("gtkmvc required version %s, found %s" % (
            request, provide))
        pass
    return


