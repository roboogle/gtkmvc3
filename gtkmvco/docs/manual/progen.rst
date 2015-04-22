progen: A Project Generator
***************************

Since version 1.2 a little application called *gtkmvc3-progen*
is provided. Goal of *gtkmvc3-progen* is to generate the skeleton
of a project that can be used when starting up a new application
based on gtkmvc3.

*gtkmvc3-progen* creates a directory containing the skeleton of a
new project, called the top-level directory.

The newly created project is constituted by:

* A source directory containing all project source code
* An empty application-level Model
* A simple application-level Controller
* The application main View containing the application main window. 
* A resources directory, containing for example the project
  glade files, but also possibly images, styles, and other resources
  loaded at runtime.
* A launching script, localized in the top-level directory


*gtkmvc3-progen* can be executed as a batch program to be
controlled from the command line, or as a simple GUI
application. *gtkmvc3-progen* is of course based on *gtkmvc3*. All
the work is performed by the model, and a view and a controller are
loaded when a GUI is required. Depending on the hosting platform,
*gtkmvc3-progen* is launched by default either in batch or in GUI
mode. Unix users are more familiar with command-line programs, and
will find *gtkmvc3-progen* to be executed in that modality by
default. Windows users will find the GUI presented by default
instead.

The way *gtkmvc3-progen* can be customized is by setting some
properties inside the model, either by using the command line, or by
using the GUI that does not export the full set of properties,
though.

Here is the list of properties with a short description:

==============  =============  ==========================================  =======
Property name   Property type  Description                                 Default value
==============  =============  ==========================================  =======
name            string         name of the project                         **REQUIRED** 
author          string         Developer's name                            **REQUIRED** 
email           string         Developer's email address 
copyright       string         Copyright string                            A sensible string
destdir         string         name of destination directory               "." 
complex         bool           Generates hierarchical MVC support          True 
dist_gtkmvc3     bool           If True, gtkmvc3 is embedded                 True 
glade           bool           if glade files are going to be used or not  True 
glade_fn        string         filename of generated glade file            application.glade 
src_header      string,None    Template for source header files.           None 
other_comment   string         Additional comment pushed after headers    
src_name        string         Name of the source directory                "src" 
res_name        string         Name of the resources directory             "resources" 
top_widget      string         Name of the View's top-level widget         "window_appl" 
==============  =============  ==========================================  =======

Bottom part of the table contains less important properties. Python
module ``gtkmv.progen.templates`` contains default templates that
are used for headers, license, etc. 

Boolean option *gui* can be used to select batch or gui
mode. Option *help* can be used to print out an helping message.




*gtkmvc3-progen* can be executed either locally (it is located
within the scripts directory), or can be executed as any other program
if *gtkmvc3* has been properly installed on the hosting system.

From the local script directory: ::

 $> (...)/scripts/gtkmvc3-progen param=val ...

If *gtkmvc3* was installed: ::

 $> gtkmvc3-progen param=val ...

Boolean properties can be specified in the form "param" or in the
form "param=[yes|no]". Specifying boolean "param" or
"param=yes" is semantically equivalent.

For example: ::

 $> gtkmvc3-progen name=hello author="Roberto Cavada" gui glade=no

The result is the creation of the top-level directory whose name is
the project name. Inside a top-level script can be used to launch
the application. 
