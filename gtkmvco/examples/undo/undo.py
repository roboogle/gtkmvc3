import locale
import random

import gtk

import _importer
import gtkmvc

from undo_manager import UndoManager

class UndoController(gtkmvc.Observer, UndoManager):
    def __init__(self):
        gtkmvc.Observer.__init__(self)
        UndoManager.__init__(self)

        self._undo_widgets = set()
        self._redo_widgets = set()

    def add_undo_widget(self, widget):
        self._undo_widgets.add(widget)
        widget.connect('clicked', self.undo_clicked)

        self.update_widgets()

    def add_redo_widget(self, widget):
        self._redo_widgets.add(widget)
        widget.connect('clicked', self.redo_clicked)

        self.update_widgets()

    def undo_clicked(self, widget):
        self.undo()

        self.update_widgets()

    def redo_clicked(self, widget):
        self.redo()

        self.update_widgets()

    def update_widgets(self):
        can_undo = self.can_undo()
        can_redo = self.can_redo()
        
        for widget in self._undo_widgets:
            widget.set_sensitive(can_undo)

        for widget in self._redo_widgets:
            widget.set_sensitive(can_redo)

    def register(self, func, *args, **kwargs):
        UndoManager.register(self, func, *args, **kwargs)

        self.update_widgets()        

    @gtkmvc.Observer.observe('*', assign=True)
    def on_assign(self, item, prop_name, info):
        self.begin_grouping()
        self.register(setattr, item, prop_name, info.old)
        self.end_grouping()

def iternames():
    """
    Monday...Sunday
    """
    for i in range(2, 8) + [1]:
        yield locale.nl_langinfo(getattr(locale, 'DAY_%i' % i))

class Day(gtkmvc.Model):
    name = ''
    hours = 0
    __observables__ = ('name', 'hours')

class Controller(gtkmvc.Controller):
    def register_view(self, view):
        self.undo = UndoController()

        self.list = gtk.ListStore(object)

        for name in iternames():
            day = Day()
            day.name = name
            self.list.append([day])
            self.undo.observe_model(day)

        view['treeview1'].set_model(self.list)
        gtkmvc.adapters.containers.watch_items_in_tree(self.list)

    def on_button3__clicked(self, widget):
        self.undo.begin_grouping()
        for row in self.list:
            row[0].hours = int(random.random() * 10)
        self.undo.end_grouping()

    def on_window1__delete_event(self, widget, event):
        gtk.main_quit()

    def register_adapters(self):
        self.setup_columns()
        self.undo.add_undo_widget(self.view['button1'])
        self.undo.add_redo_widget(self.view['button2'])

Controller(gtkmvc.Model(), gtkmvc.View(builder='undo.ui'), handlers='class')

gtk.main()
