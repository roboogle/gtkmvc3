__all__ = ("add_adapter", "remove_adapter", "search_adapter_info",
           "SIGNAL", "GETTER", "SETTER", "WIDTYPE", "FLAVOUR")


from gi.repository import Gtk, Gdk


def __radio_setter_label(radio, value):
    # this is used to control RadioButton and RadioAction
    if radio.get_label() == value:
        radio.set_active(True)


def __radio_getter_label(radio):
    # this is used to control RadioButton and RadioAction
    if radio.get_active():
        return radio.get_label()
    raise ValueError("Radio not active")


def __radio_action_setter_value(ra, value):
    if value == ra.get_property("value"):
        ra.set_active(True)
    return


def __radio_action_getter_value(ra):
    if ra.get_active():
        return ra.get_current_value()
    raise ValueError("RadioAction not active")


# ----------------------------------------------------------------------
# This list defines a default behavior for widgets.
# If no particular behaviour has been specified, adapters will
# use information contained into this list to create themself.
# This list is ordered: the earlier a widget occurs, the sooner it
# will be matched by the search function.
# ----------------------------------------------------------------------
__def_adapter = [ # class, default signal, getter, setter, value type, flavour

    (Gtk.Entry, "changed", Gtk.Entry.get_text, Gtk.Entry.set_text, str, None),

    (Gtk.Label, None, Gtk.Label.get_text, Gtk.Label.set_text, str, None),

    (Gtk.Arrow, None, lambda a: a.get_property("arrow-type"),
     lambda a,v: a.set(v,a.get_property("shadow-type")), Gtk.ArrowType, None),

    (Gtk.RadioAction, "toggled", __radio_action_getter_value, __radio_action_setter_value, int, "value"),
    (Gtk.RadioAction, "toggled", Gtk.RadioAction.get_active, Gtk.RadioAction.set_active, bool, "active"),
    (Gtk.RadioAction, "toggled", __radio_getter_label, __radio_setter_label, str, None),

    (Gtk.RadioButton, "toggled", Gtk.RadioButton.get_active, Gtk.RadioButton.set_active, bool, "active"),
    (Gtk.RadioButton, "toggled", __radio_getter_label, __radio_setter_label, str, None),

    (Gtk.RadioToolButton, "toggled", Gtk.RadioToolButton.get_active, Gtk.RadioToolButton.set_active, bool, "active"),

    (Gtk.ToggleButton, "toggled", Gtk.ToggleButton.get_active, Gtk.ToggleButton.set_active, bool, None),
    (Gtk.ToggleAction, "toggled", Gtk.ToggleAction.get_active, Gtk.ToggleAction.set_active, bool, None),
    (Gtk.ToggleToolButton, "toggled", Gtk.ToggleToolButton.get_active, Gtk.ToggleToolButton.set_active, bool, None),

    (Gtk.CheckMenuItem, "toggled", Gtk.CheckMenuItem.get_active, Gtk.CheckMenuItem.set_active, bool, None),

    (Gtk.Expander, "activate", lambda w: not w.get_expanded(), Gtk.Expander.set_expanded, bool, None),

    (Gtk.ColorButton, "color-set", Gtk.ColorButton.get_color, Gtk.ColorButton.set_color, Gdk.Color, None),

    (Gtk.ColorSelection, "color-changed", Gtk.ColorSelection.get_current_color, Gtk.ColorSelection.set_current_color, Gdk.Color, None),

    (Gtk.ComboBox, "changed", Gtk.ComboBox.get_active, Gtk.ComboBox.set_active, int, None),

    (Gtk.Adjustment, "value-changed", Gtk.Adjustment.get_value, Gtk.Adjustment.set_value, float, None),

    (Gtk.FileChooserButton, "selection-changed", Gtk.FileChooserButton.get_filename, Gtk.FileChooserButton.set_filename, str, None),

    (Gtk.LinkButton, "clicked", Gtk.LinkButton.get_uri, Gtk.LinkButton.set_uri, str, None),
    ]


# constants to access values:
WIDGET, SIGNAL, GETTER, SETTER, WIDTYPE, FLAVOUR = range(6)
# ----------------------------------------------------------------------

def add_adapter(widget_class, signal_name, getter, setter, value_type,
                flavour=None):
    """This function can be used to extend at runtime the set of
    default adapters. If given widget class which is being added is
    already in the default set, it will be substituted by the new one
    until the next removal (see remove_adapter).

    @param flavour can be used to differentiate otherwise identical
    entries (None for no flavour)."""

    new_tu = (widget_class, signal_name, getter, setter,
              value_type, flavour)
    for it,tu in enumerate(__def_adapter):
        if issubclass(tu[WIDGET], widget_class):
            # found an insertion point, iteration is over after inserting
            __def_adapter.insert(it, new_tu)
            return

    # simply append it
    __def_adapter.append(new_tu)


def remove_adapter(widget_class, flavour=None):
    """Removes the given widget class information from the default set
    of adapters.

    If widget_class had been previously added by using add_adapter,
    the added adapter will be removed, restoring possibly previusly
    existing adapter(s). Notice that this function will remove only
    *one* adapter about given wiget_class (the first found in order),
    even if many are currently stored.

    @param flavour has to be used when the entry was added with a
    particular flavour.

    Returns True if one adapter was removed, False if no adapter was
    removed."""
    for it,tu in enumerate(__def_adapter):
        if (widget_class == tu[WIDGET] and flavour == tu[FLAVOUR]):
            del __def_adapter[it]
            return True

    return False # no adapter was found


# To optimize the search
__memoize__ = {}
def search_adapter_info(wid, flavour=None):
    """Given a widget returns the default tuple found in __def_adapter.

    @param flavour can be used to specialize the search for a
    particular tuple.
    """
    t = (type(wid), flavour)
    if t in __memoize__:
        return __memoize__[t]

    for w in __def_adapter:
        if (isinstance(wid, w[WIDGET]) and flavour == w[FLAVOUR]):
            __memoize__[t] = w
            return w

    raise TypeError("Adapter type " + str(t) + " not found among supported adapters")
