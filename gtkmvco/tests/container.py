## Started on  Thu Dec  3 09:20:42 2009 Roberto Cavada
## Copyright (C) 2009 Roberto Cavada

import _importer
from gtkmvc import Model, Observer

class MyModel(Model):
    seq = []
    dic = {}
    __observables__ = ("seq", "dic")
    pass

class MyObserver(Observer):
    seq_calls = 0
    dic_calls = 0
    def property_seq_before_change(self, model, instance, name, args, kwargs):
        self.seq_calls += 1
        return

    def property_dic_after_change(self, model, instance, name, res, args, kwargs):
        self.dic_calls += 1
        return
    pass

# tests begin
import unittest
class TestSeq(unittest.TestCase):   
    seq = range(5)
    dic = dict(zip(map(str, seq), seq))
    def setUp(self):
        self.m = MyModel()
        self.o = MyObserver(self.m)

        self.m.seq = []
        for i in self.seq:
            self.m.seq.append(i)
            self.m.dic[str(i)] = i
        return
    
    def testcmp(self):
        # checks comparison
        self.assert_(self.m.seq < list(self.seq) + [1])
        self.assert_(self.m.seq <= list(self.seq))
        self.assert_(self.m.seq == list(self.seq))
        self.assert_(self.m.seq >= list(self.seq))
        self.assert_(self.m.seq > list(self.seq)[:-1])
        self.assert_(self.m.seq != list(self.seq[:-1]))

        self.assert_(self.m.dic == self.dic)
        return

    def testnotify(self):
        # tests notifications have been processed
        self.assertEqual(self.o.seq_calls, len(self.seq))
        self.assertEqual(self.o.dic_calls, len(self.dic))
        return

    def testlen(self):
        self.assertEqual(len(self.m.seq), len(self.seq))
        self.assertEqual(len(self.m.dic), len(self.dic))
        return
    
    def testiteration(self):
        for i,j in zip(self.seq, self.m.seq): self.assertEqual(i, j)
        for i,j in zip(self.dic, self.m.dic): self.assertEqual(i, j)
        return
        
    def testcontains(self):
        for i in self.seq: self.assert_(i in self.m.seq)
        for i in self.dic: self.assert_(i in self.m.dic)
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
    
    
if __name__ == "__main__":
    unittest.main()

