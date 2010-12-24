
=============================================
Error and Warning conditions with logical OPs
=============================================

When dealing with logical OPs and in particular with getter/setter
pairs, there are complex conditions and behaviours of the framework
which may be confusing. Here those conditions are listed and
explained.

Error conditions
----------------

* **A logical OP has no associated getter.**
 
  Getters are mandatory for logical OPs.

* **OP matched by multiple getters/setters.**

  Each OP must be matched exactly with one getter and optionally with
  one setter. It is an error condition any multiple matching.

* **Exactly the same pattern was used for one or more getters (setters).**

  This is a specialization of previous case (multiple matching).


Warning conditions
------------------

Warning are issued only if the devlopers enables them. In released
applications, warnings should be not visible by default, to avoid
worrying the application user.

When developing, it is important to enable warnings, though.

* **A setter has no corresponing getter.**

  When a setter has no getter, the setter is simply ignored.

* **Getter/setter defined for concrete OPs.**

  When a getter and/or a setter is defined for a concrete OP (not a
  *logical* OP), the getter/setter are ignored.

* **Getter/setter defined for non-existing logical OP.**

  Getters/setters whose pattern do not match any existing logical OP,
  are ignored.

