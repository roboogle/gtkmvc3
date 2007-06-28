__all__ = ("search_adapter_info",
           "SIGNAL", "GETTER", "SETTER", "WIDTYPE")

import types
import gtk

# ----------------------------------------------------------------------
# This list defines a default behavior for widgets.
# If no particular behaviour has been specified, adapters will
# use information contained into this list to create themself.
# This list is ordered: the earlier a widget occurs, the better it
# will be matched by the search function. 
# ----------------------------------------------------------------------
__def_adapter = ( # class, default signal, getter, setter, value type
    (gtk.Entry, "changed", gtk.Entry.get_text, gtk.Entry.set_text, types.StringType),
    (gtk.Label, None, gtk.Label.get_text, gtk.Label.set_text, types.StringType),
    
    
    )

# constants to access values:
SIGNAL  =1
GETTER  =2
SETTER  =3
WIDTYPE =4
# ----------------------------------------------------------------------


# To optimize the search
__memoize__ = {}    
def search_adapter_info(wid):
    """Given a widget returns the default tuple found in __def_adapter""" 
    t = type(wid)
    if __memoize__.has_key(t): return __memoize__[t]

    for w in __def_adapter:
        if isinstance(wid, w[0]):
            __memoize__[t] = w
            return w
        pass

    raise TypeError("Adapter type " + str(t) + " not found among supported adapters")
        
