class Node(object):
    def __init__(self, name, children=()):
        self.name = name
        self.children = list(children)

    def __str__(self):
        return '<Node %s>' % self.name


class Visitor(object):

    @classmethod
    def visit(cls, node):
        yield node
        for child in node.children:
            yield child

    @classmethod
    def visit2(cls, node):
        for child in node.children:
            yield child
        yield node


if __name__ == '__main__':
    root = Node('root', (Node('a'), Node('b')))
    visitor = Visitor()
    for node in visitor.visit(root):
        print(node)
    for node in visitor.visit2(root):
        print(node)
