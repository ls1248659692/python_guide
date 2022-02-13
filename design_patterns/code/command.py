from collections import deque


class Document(object):
    value = ""
    cmd_stack = deque()

    @classmethod
    def execute(cls, cmd):
        cmd.redo()
        cls.cmd_stack.append(cmd)

    @classmethod
    def undo(cls):
        cmd = cls.cmd_stack.pop()
        cmd.undo()


class AddTextCommand(object):
    def __init__(self, text):
        self.text = text

    def redo(self):
        Document.value += self.text

    def undo(self):
        Document.value = Document.value[:-len(self.text)]


if __name__ == '__main__':
    cmds = [AddTextCommand("liu"), AddTextCommand("xin"), AddTextCommand("heihei")]
    for cmd in cmds:
        Document.execute(cmd)
        print(Document.value)

    for i in range(len(cmds)):
        Document.undo()
        print(Document.value)
