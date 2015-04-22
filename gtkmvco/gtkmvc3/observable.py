#  -------------------------------------------------------------------------
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
#  51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.ridge, MA 02139, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author <roboogle@gmail.com>.
#  -------------------------------------------------------------------------


from gtkmvc3.support import decorators, log
from gtkmvc3.support.wrappers import ObsWrapperBase


class Observable (ObsWrapperBase):

    @classmethod
    @decorators.good_classmethod_decorator
    def observed(cls, _func):
        """
        Decorate methods to be observable. If they are called on an instance
        stored in a property, the model will emit before and after
        notifications.
        """

        def wrapper(*args, **kwargs):
            self = args[0]
            assert(isinstance(self, Observable))

            self._notify_method_before(self, _func.__name__, args, kwargs)
            res = _func(*args, **kwargs)
            self._notify_method_after(self, _func.__name__, res, args, kwargs)
            return res

        return wrapper


    def __init__(self):
        ObsWrapperBase.__init__(self)

# ----------------------------------------------------------------------


@decorators.good_decorator
def observed(func):
    """
    Just like :meth:`Observable.observed`.

    .. deprecated:: 1.99.1
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        assert(isinstance(self, Observable))

        self._notify_method_before(self, func.__name__, args, kwargs)
        res = func(*args, **kwargs)
        self._notify_method_after(self, func.__name__, res, args, kwargs)
        return res

    log.logger.warning("Decorator observable.observed is deprecated:"
                       "use Observable.observed instead")
    return wrapper


# ----------------------------------------------------------------------
class Signal (Observable):
    """Base class for signals properties"""
    def __init__(self):
        Observable.__init__(self)

    def emit(self, arg=None):
        """Emits the signal, passing the optional argument"""
        for model,name in self.__get_models__():
            model.notify_signal_emit(name, arg)
