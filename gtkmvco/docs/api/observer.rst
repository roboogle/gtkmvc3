Observers
=========

.. module:: gtkmvc.observer

.. autofunction:: observes(*args)

.. autoclass:: Observer
    :members:
    :exclude-members: get_custom_observing_methods
    :undoc-members:

    .. method:: get_custom_observing_methods(prop_name)

       An alias for :meth:`get_observing_methods`.

       .. deprecated:: 1.99.1

.. autoclass:: NTInfo
    :show-inheritance:

    .. automethod:: __getattr__
