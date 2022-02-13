class Implementation(object):
    def add(self, x, y):
        return x + y

    def minus(self, x, y):
        return x - y


class Proxy(object):
    def __init__(self, impl):
        self._impl = impl

    def __getattr__(self, name):
        return getattr(self._impl, name)


if __name__ == '__main__':
    p = Proxy(Implementation())
    print(p.add(1, 2))
    print(p.minus(1, 2))
