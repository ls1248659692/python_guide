class Observable(object):

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


class Observer(object):
    def update(self, observable):
        print('updating %s by %s' % (self, observable))


if __name__ == '__main__':
    clock = Observable()
    user1 = Observer()
    user2 = Observer()
    clock.attach(user1)
    clock.attach(user2)
    clock.notify()
