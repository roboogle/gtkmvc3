Model Classes
=============

There are several possible ways to derive your model. All look the same
to a :class:`Controller`.

.. module:: gtkmvc.model

.. autoclass:: Model
    :members:
    :undoc-members:
    :show-inheritance:

Persistence
-----------

.. autoclass:: SQLObjectModel
    :show-inheritance:

    .. automethod:: createTables

Specific widgets
----------------

.. autoclass:: TextBufferModel
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: ListStoreModel
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: TreeStoreModel
    :members:
    :undoc-members:
    :show-inheritance:

Threading
---------

.. module:: gtkmvc.model_mt

.. autoclass:: ModelMT

.. autoclass:: TextBufferModelMT

.. autoclass:: ListStoreModelMT

.. autoclass:: TreeStoreModelMT
