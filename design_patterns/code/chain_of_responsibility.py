class Handler(object):

    def __init__(self):
        self.successor = None

    def handle(self, data):
        res = self._handle(data)
        if res:
            return res
        if self.successor:
            return self.successor.handle(data)

    def _handle(self, data):
        raise NotImplementedError

    def link(self, handler):
        self.successor = handler
        return handler


class DictHandler(Handler):
    def _handle(self, data):
        if isinstance(data, dict):
            print("handled by %s" % self)
            return True


class ListHandler(Handler):
    def _handle(self, data):
        if isinstance(data, list):
            print("handled by %s" % self)
            return True


if __name__ == '__main__':
    h = DictHandler()
    h.link(ListHandler()).link(Handler())
    ret = h.handle([1, 2, 3])
    ret = h.handle({1: 2})
