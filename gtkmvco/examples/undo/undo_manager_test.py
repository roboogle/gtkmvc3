import unittest

from undo_manager import UndoManager

class InitialTest(unittest.TestCase):
    def setUp(self):
        self.m = UndoManager()

    def testCan(self):
        self.assertFalse(self.m.can_redo())
        self.assertFalse(self.m.can_undo())

    def testEnd(self):
        self.assertRaises(IndexError, self.m.end_grouping)

    def testLevel(self):
        self.assertEqual(0, self.m.grouping_level())

    def testDoing(self):
        self.assertFalse(self.m.is_redoing())
        self.assertFalse(self.m.is_undoing())

    def testRedo(self):
        self.m.redo()

    def testUndo(self):
        self.m.undo()

    def testName(self):
        self.assertEqual("", self.m.redo_action_name())
        self.assertEqual("", self.m.undo_action_name())

    def testRegister(self):
        self.assertRaises(IndexError, lambda: self.m.register(None))

    def testSetName(self):
        self.m.set_action_name("Hello")

    def testUndoGroup(self):
        self.m.undo_nested_group()

class GroupTest(unittest.TestCase):
    def setUp(self):
        self.t = ""
        self.m = UndoManager()
        self.m.begin_grouping()
        self.type("H")
        self.m.set_action_name("Type H")

    def type(self, char):
        self.t += char
        self.m.register(self.backspace)

    def backspace(self):
        self.m.register(self.type, self.t[-1])
        self.t = self.t[:-1]

    def testState(self):
        self.assertFalse(self.m.can_redo())
        self.assertTrue(self.m.can_undo())
        self.assertEqual(1, self.m.grouping_level())
        self.assertFalse(self.m.is_redoing())
        self.assertFalse(self.m.is_undoing())
        self.assertEqual("", self.m.redo_action_name())
        self.assertEqual("Type H", self.m.undo_action_name())

    def testUndo(self):
        self.m.undo()

        self.assertEqual("", self.t)
        self.assertTrue(self.m.can_redo())
        self.assertFalse(self.m.can_undo())
        self.assertEqual(0, self.m.grouping_level())
        self.assertFalse(self.m.is_redoing())
        self.assertFalse(self.m.is_undoing())
        self.assertEqual("Type H", self.m.redo_action_name())
        self.assertEqual("", self.m.undo_action_name())

    def testRedo(self):
        self.m.undo()
        self.m.redo()

        self.assertFalse(self.m.can_redo())
        self.assertTrue(self.m.can_undo())
        self.assertEqual(0, self.m.grouping_level())
        self.assertFalse(self.m.is_redoing())
        self.assertFalse(self.m.is_undoing())
        self.assertEqual("", self.m.redo_action_name())
        self.assertEqual("Type H", self.m.undo_action_name())

    def testStress(self):
        self.m.end_grouping()
        self.m.begin_grouping()
        for c in "ello World":
            self.type(c)
        self.m.end_grouping()
        self.assertEqual("Hello World", self.t)
        self.m.undo()
        self.assertEqual("H", self.t)
        self.assertTrue(self.m.can_redo())

if __name__ == "__main__":
    unittest.main()
