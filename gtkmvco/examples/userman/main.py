import gtk

import _importer # this is an helper to import gtkmvc3

from model import ExampleModel
from ctrl import ExampleController
from view import ExampleView

import gtkmvc3

def check_requirements():
    gtkmvc3.require("1.0.0")
    return

def setup_env(development_state=False):
    # This is how developers should set gtkmvc3 logging level (by
    # default debugging info is not shown):
    if development_state:
        import logging
        logging.getLogger("gtkmvc3").setLevel(logging.DEBUG)
        pass
    return

def main():
    m = ExampleModel()
    v = ExampleView()
    c = ExampleController(m, v)

    gtk.main()
    return

if __name__ == "__main__":
    check_requirements()
    setup_env(development_state=True)
    main()
    pass

