Motivations
***********

One major effort of Software Engineering has been to provide a way of
optimally separating the logical parts that constitute a software.
This issue becomes a question of outstanding importance in
middle/large interactive software, where an agent like an human user
interacts with the software, likely through a Graphic User Interface
(*GUI*).
To separate the logic (data) of an application from the representation
of those data, several Architectural Patterns [#archipat]_
have been studied; one is the Model--View--Controller (MVC) pattern
that splits the application into three separate parts, the *Model*,
the *View* and the *Controller*. The level of mutual knowledge
among these three entities is kept as minimal as possible, and this
results in:

* Reduced wrong dependencies.
* Software architecture forced to be better designed.
* Minimized propagation of changes/modifications.
* Higher costs of startup, but potential lower costs of
  maintenance.


To improve re-usability and robustness of software, the *Observer* pattern is used
as well. This pattern identifies two entities: the
*Observable data* and the *Observer* over those data.

The implementation of the *Observer* pattern is intended to make the Observer take
some action when the Observable data change. This triggering mechanism
is a further abstraction layer that helps to
design and implement robust software.

A possible use of the *Observer* pattern is in combination with the *MVC* pattern, where the
model communicates indirectly with the presentation side through the
observer pattern.


*gtkmvc3* is a framework that implements both the MVC and Observer
patterns to be used to produce middle/large applications in Python and
*PyGTK*.

The main goal is to provide a minimal (but not trivial)
implementation, where practical aspects are taken into serious
consideration, and complexity is kept behind the scene. This makes the
users able to mainly focus their attention on the application they
need to produce, instead of dealing with the underlying framework.


Pointless to say that goals are clear and likely easy to
share by anyone. It is quite a different thing to prove that those
goals are reached by the proposed framework. Frankly, this is up to
the reader to decide.

.. rubric:: Footnotes

.. [#archipat] http://en.wikipedia.org/wiki/Architectural_pattern_(computer_science%29
