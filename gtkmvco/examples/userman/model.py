import _importer # this is an helper to import gtkmvc3
from gtkmvc3 import Model

class ExampleModel (Model):
    """The model contains a set of messages
    and an observable property that represent the current message
    index"""

    # Observable property: code for that is automatically generated
    # by metaclass constructor. The controller will be the observer
    # for this property
    message_index = -1   # -1 is the initial value
    __observables__ = ("message_index",)

    def __init__(self):
        Model.__init__(self)

        self.messages= ("I am patient with stupidity",
                        "but not with those",
                        "who are proud of it.",
                        "(Edith Sitwell)",
                        )
        return

    def get_message(self, index): return self.messages[index]

    def set_next_message(self):
        # this changes the observable property:
        self.message_index = (self.message_index + 1) % len(self.messages)
        return

    pass # end of class
