import gtk

import _importer # this is an helper to import gtkmvc

from model import ExampleModel
from ctrl import ExampleController
from view import ExampleView

import gtkmvc

def check_requirements():
    gtkmvc.require("1.99.1")
    return

def setup_env(development_state=False):
    # This is how developers should set gtkmvc logging level (by
    # default debugging info is not shown):
    if development_state:
        import logging
        logging.getLogger("gtkmvc").setLevel(logging.DEBUG)
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

