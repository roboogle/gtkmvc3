from functools import partial as UndoOperation

class UndoGroup(list):
    name = ""

    def perform(self):
        for operation in reversed(self):
            operation()

class UndoManager(object):
    """
    An action by the user may result in multiple operations.
    """

    def __init__(self):
        self._undo = []
        self._redo = []
        self._open = []
        self._redoing = False
        self._undoing = False

    def begin_grouping(self):
        """
        Each undo operation has to be in a group. Groups can be nested.
        """
        self._open.append(UndoGroup())

    def can_redo(self):
        """
        Are there actions to redo?
        """
        return bool(self._redo)

    def can_undo(self):
        """
        Are there actions to undo?
        """
        return bool(self._undo) or bool(self._open and self._open[0])

    def end_grouping(self):
        """
        Raises IndexError when no group is open.
        """
        close = self._open.pop()
        if not close:
            return
        if self._open:
            self._open[-1].extend(close)
        elif self._undoing:
            self._redo.append(close)
        else:
            self._undo.append(close)

    def grouping_level(self):
        """
        How many groups are open?
        """
        return len(self._open)

    def is_redoing(self):
        """
        Are we performing a redo?
        """
        return self._redoing

    def is_undoing(self):
        """
        Are we performing an undo?
        """
        return self._undoing

    def redo(self):
        """
        Performs the top group on the redo stack, if present. Creates an undo
        group with the same name. Raises RuntimeError if called while undoing.
        """
        if self._undoing or self._redoing:
            raise RuntimeError
        if not self._redo:
            return
        group = self._redo.pop()

        stack = self._open
        self._redoing = True

        self.begin_grouping()
        group.perform()
        self.set_action_name(group.name)
        self.end_grouping()

        self._redoing = False
        self._open = stack

    def redo_action_name(self):
        """
        The name of the top group on the redo stack, or an empty string.
        """
        if self._redo:
            return self._redo[-1].name
        return ""

    def register(self, func, *args, **kwargs):
        """
        Record an undo operation. Also clears the redo stack. Raises IndexError
        when no group is open.
        """
        self._open[-1].append(UndoOperation(func, *args, **kwargs))
        if not (self._undoing or self._redoing):
            self._redo = []

    def set_action_name(self, name):
        """
        Set the name of the top group, if present.
        """
        if self._open and name is not None:
            self._open[-1].name = name

    def undo(self):
        """
        Raises IndexError if more than one group is open, otherwise closes it
        and invokes undo_nested_group.
        """
        if self.grouping_level() == 1:
            self.end_grouping()
        if self._open:
            raise IndexError
        self.undo_nested_group()

    def undo_action_name(self):
        """
        The name of the top group on the undo stack, or an empty string.
        """
        if self._open:
            return self._open[-1].name
        elif self._undo:
            return self._undo[-1].name
        return ""

    def undo_nested_group(self):
        """
        Performs the last group opened, or the top group on the undo stack.
        Creates a redo group with the same name.
        """
        if self._undoing or self._redoing:
            raise RuntimeError
        if self._open:
            group = self._open.pop()
        elif self._undo:
            group = self._undo.pop()
        else:
            return

        stack = self._open
        self._undoing = True

        self.begin_grouping()
        group.perform()
        self.set_action_name(group.name)
        self.end_grouping()

        self._undoing = False
        self._open = stack
