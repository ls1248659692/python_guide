# encoding=utf-8


class SingletonMeta(type):

    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.instance


class CurrentUser(object, metaclass=SingletonMeta):

    def __init__(self, name=None):
        super(CurrentUser, self).__init__()
        self.name = name

    def __str__(self):
        return repr(self) + ":" + repr(self.name)


if __name__ == '__main__':
    u = CurrentUser("liu")
    print(u)
    u2 = CurrentUser()
    u2.name = "xin"
    print(u2)
    print(u)
    assert u is u2
