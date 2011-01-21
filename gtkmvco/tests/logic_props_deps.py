"""
Test for dependencies of logical properties
"""

import _importer
from gtkmvc import Model

import unittest

class LinearSingleLevel (Model):
    conc = 0

    __observables__ = "conc log1".split()

    @Model.getter(deps=["conc"])
    def log1(self): return self.conc+1

    @Model.getter(deps=["log1"])
    def log2(self): return self.log1+1
    pass

class LinearMultiLevel (Model):
    conc = 0

    __observables__ = "conc log1 log2".split()

    @Model.getter(deps=["conc"])
    def log1(self): return self.conc+1

    @Model.getter(deps=["log1"])
    def log2(self): return self.log1+1

    @Model.getter(deps=["log2"])
    def log3(self): return self.log2+1
    pass

class BranchSingleLevel (Model):
    conc1 = 0
    conc2 = 1

    __observables__ = "conc? log1 log2 log3".split()
    
    @Model.getter(deps=["conc1"])
    def log1(self): return self.conc1+1

    @Model.getter(deps=["conc1"])
    def log2(self): return self.conc1+1

    @Model.getter(deps=["conc1", "conc2"])
    def log3(self): return self.conc1+self.conc2
    pass

class BranchMultiLevel (Model):
    conc1 = 0
    conc2 = 1

    __observables__ = "conc? log1 log2 log3".split()
    
    @Model.getter(deps=["conc1"])
    def log1(self): return self.conc1+1

    # here there is a diamond
    @Model.getter(deps=["conc1", "conc2", "log1"])
    def log2(self): return self.conc1+self.conc2+self.log1

    @Model.getter(deps=["log2"])
    def log3(self): return self.log2    
    pass

# must raise ValueError
class InvalidLoop (Model):
    conc = 0
    __observables__ = "conc log1 log2 log3".split()

    @Model.getter(deps=["conc1", "log3"])
    def log1(self): return self.conc1+1

    @Model.getter(deps=["log1"])
    def log2(self): return self.conc1+1

    @Model.getter(deps=["log2"])
    def log3(self): return self.conc1+1
    pass

# must raise TypeError:
#class InvalidSyntax (Model):
#    conc = 0
#    __observables__ = "conc log1".split()

#    @Model.getter(deps=[1])
#    def log1(self): return self.conc1+1

#m = BranchMultiLevel()
