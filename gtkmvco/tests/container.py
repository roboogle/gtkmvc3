## Started on  Thu Dec  3 09:20:42 2009 Roberto Cavada
## Copyright (C) 2009 Roberto Cavada

import _importer
from gtkmvc import Model, Observer

class MyModel(Model):
    seq = []
    __observables__ = ("seq", )
    pass

class MyObserver(Observer):
    calls = 0
    def property_seq_before_change(self, model, instance, name, args, kwargs):
        self.calls += 1
        return
    pass

# tests begin
import unittest
class TestSeq(unittest.TestCase):   
    seq = range(5)

    def setUp(self):
        self.m = MyModel()
        self.o = MyObserver(self.m)

        self.m.seq = []
        for i in self.seq: self.m.seq.append(i)
        return
    
    def testcmp(self):
        # checks insertions
        self.assert_(self.m.seq < list(self.seq) + [1])
        self.assert_(self.m.seq <= list(self.seq))
        self.assert_(self.m.seq == list(self.seq))
        self.assert_(self.m.seq >= list(self.seq))
        self.assert_(self.m.seq > list(self.seq)[:-1])
        self.assert_(self.m.seq != list(self.seq[:-1]))
        return

    def testnotify(self):
        # tests notifications have been processed
        self.assertEqual(self.o.calls, len(self.seq))
        return

    def testlen(self):
        self.assertEqual(self.o.calls, len(self.seq))
        return
    
    def testiteration(self):
        for i,j in zip(self.seq, self.m.seq): self.assertEqual(i, j)
        return
        
    def testcontains(self):
        for i in self.seq: self.assert_(i in self.m.seq)
        return

    def testops(self):
        ad = [1,2]
        self.assertEqual(len(self.m.seq + ad), len(self.m.seq) + len(ad))
        self.assertEqual(len(ad + self.m.seq), len(self.m.seq) + len(ad))
        self.assertEqual(len(self.m.seq * 5), len(self.m.seq) * 5)
        self.assertEqual(len(5 * self.m.seq), len(self.m.seq) * 5)
        return
    
    def testaugmented(self):
        self.m.seq += [10]
        self.assert_(10 in self.m.seq)

        self.m.seq *= 2
        self.assert_(self.m.seq.count(1) == 2)
        return

    def testindex(self):
        self.assertEqual(self.m.seq.index(2), 2)
        return

    def testslice(self):
        self.assertEqual(self.m.seq[1:2], list(self.seq)[1:2])
        self.assertEqual(self.m.seq[1:-1], list(self.seq)[1:-1])

        self.m.seq[2:3] = [20,30]
        self.assertEqual(self.m.seq[2:4], [20,30])
        return

    def testreversed(self):
        self.assertEqual(list(reversed(self.m.seq)), list(reversed(self.seq)))
        return
    
    
unittest.main()

