.. _step2:

########################
A short tutorial: Step 2
########################

.. include:: common.rst 

In :ref:`first part<step1>` we have seen a simple example. 

In this section we will see a more complex example. In particular we
will make an more advanced use of :ref:`adapters`, and :ref:`OP_log`
with :ref:`OP_log_deps`.


The example illustrated
=======================

In this example, we want to show a set of *counters*. These are the requisites:

Requisites about the *logic*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. There are a variable number of counters in the set.

2. Each counter is identified by a unique name. 

3. Each counter counts from 0 to a maximum number (which may depend on
   the specific counter).

4. Each counter must be selected (through its name) before being used.

5. Each counter can be reset (to 0) and incremented (by 1). When the
   maximum number is reached, any further increment produces no
   effects.

Requisites about the *view*
~~~~~~~~~~~~~~~~~~~~~~~~~~~

6. The user can selects the current counter.

7. The user can increment and reset the currently selected counter.

8. The user sees the currently selected counter, and its current value. 

9. The user receives feedback when the counter is closed to the
   maximum value, and when it reached the maximum value.

.. _fig_appl2:

.. figure:: images/appl2_ann.png
   :width: 12cm

   How the view looks like

   Here you can see how the application looks like, and the
   highlighted regions have correspondences in the view requisites
   6-9.

.. _fig_step2_window:

.. figure:: images/step2_window_top.png
   :width: 8cm

   The main window in |glade|

   In picture :ref:`fig_step2_window` you can see how the main top
   level window looks like in |glade|. Here the format chosen is
   `gtk.Builder` as objects are needed as well (see
   :ref:`fig_step2_hierarchy` below).

   The big area in the middle is represented by the `gtk.VBox` widget
   named `vbox_rb` and its purpose is to contain the radio buttons for
   selecting the current counter.

   Here requisite 1 specifies that the number of counters is
   *variable*, meaning that it cannot be determined statically. For
   this reason the view will be filled with the required
   `gtk.RadioButton`s when the view will be instantiated and connected
   to the model which contains the actual counters.

   The top level window contains also:

   * A `gtk.Label` for the name of the currently selected counter.

   * A  `gtk.Label` for the value of the currently selected counter.

   * A `gtk.ProgressBar` for the value of the currently selected counter.

   * A `gtk.Image` for giving feedback to the user about the value of
     the currently selected counter.

   * A `gtk.Entry` as an alternative way of selecting the current counter.

.. _fig_step2_hierarchy:

.. figure:: images/step2_hierarchy.png 
   :height: 14cm

   The widgets and objects in |glade|

   

