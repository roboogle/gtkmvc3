"""
Test should print:
<class '__main__.AA'>
<unbound method AA.foo>
foo
"""


class Meta (type):

  def __new__(cls, name, bases, cls_dict):

    
    clsi = type.__new__(cls, name, bases, cls_dict)
    print clsi

    def foo(self): print "foo"
    setattr(clsi, "foo", foo)
    
    return clsi

  
  pass


class AA (object):
  __metaclass__ = Meta

  pass

print AA.foo
a = AA()
a.foo()
