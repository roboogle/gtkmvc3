import _importer # this is an helper to import gtkmvc3
from gtk import main_quit
from gtkmvc3 import Controller

class ExampleController(Controller):
    """The only one controller. Handles the button clicked signal, and
    notifications about one observable property."""

    def __init__(self, model, view):
        """Contructor. model will be accessible via the member 'self.model'.
        View registration is also performed."""
        Controller.__init__(self, model, view)
        return

    def register_view(self, view):
        # Connects the exiting signal:
        view.get_top_widget().connect("destroy", main_quit)
        return

    # Signal
    def on_button1_clicked(self, button):
        """Handles the signal clicked for button1. Changes the model."""
        self.model.set_next_message()
        return

    # Observables notifications
    @Controller.observe("message_index", assign=True)
    def value_change(self, model, name, info):
        """The model is changed and the view must be updated"""
        msg = self.model.get_message(info.new)

        self.view.set_msg(msg)
        return

    pass # end of class
