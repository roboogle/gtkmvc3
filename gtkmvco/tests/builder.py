import unittest

import gtk

class Controller(object):
    def __init__(self):
        self.events = {}

    def on_button7_clicked(self, button, data):
        try:
            self.events[data] += 1
        except KeyError:
            self.events[data] = 1

class BuilderTest(unittest.TestCase):
    def setUp(self):
        self.x = gtk.Builder()
        self.x.add_from_file('adapter19.ui')
        self.b = self.x.get_object('button7')
        self.c = Controller()

    def testTwice(self):
        self.x.connect_signals(self.c, 1)
        self.x.connect_signals(self.c, 2)

        self.b.clicked()
        # Undocumented feature!
        self.assertEqual({1: 1}, self.c.events)

    def testManual(self):
        self.b.connect('clicked', self.c.on_button7_clicked, 3)
        self.b.connect('clicked', self.c.on_button7_clicked, 4)

        self.b.clicked()
        self.assertEqual({3: 1, 4:1}, self.c.events)

    def testMix(self):
        self.x.connect_signals(self.c, 5)
        self.b.connect('clicked', self.c.on_button7_clicked, 6)

        self.b.clicked()
        # Would have been nice...
        self.assertEqual({5: 1, 6:1}, self.c.events)

if __name__ == "__main__":
    unittest.main()
