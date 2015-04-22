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
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.


try: import threading as _threading
except ImportError: import dummy_threading as _threading
import time


from gtkmvc3 import ModelMT
class MyModel (ModelMT):
    """Our model derives from ModelMT instead of from Model, as the
    model is being changed by a thread different from the thread
    running the gtk main loop. This would be not a problem, if there
    was not an observer (the controller) that needs to access gtk
    functions, so needs to run in the same thread of gtk main loop.
    This requires to isolate the thread changing the model from the
    thread which the controller runs in. This insulation is carried
    out transparently by class ModelMT that out model derives from."""

    counter = 0
    busy = False
    __observables__ = ('counter', 'busy')
    
    def __init__(self):
        ModelMT.__init__(self)
        self.thread = None # the thread that runs our test
        return

    def run_test(self):
        """This is called to start a new test"""
        if self.busy: return # currently running, exit
        self.thread = _threading.Thread(target=self.run)
        self.thread.start()
        return

    def run(self):
        """This method is run by a separated thread"""
        self.busy = True

        for i in range(9):
            self.counter += 1
            time.sleep(0.5)
            pass
        self.counter += 1
        
        self.busy = False
        return
    
    pass # end of class

