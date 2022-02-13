# encoding=utf-8


class ApplicateFramework(object):
    def __init__(self):
        self.setup()
        self.show()

    def setup(self):
        pass

    def show(self):
        pass

    def close(self):
        pass


class MyApplication(ApplicateFramework):
    def setup(self):
        print("setup", self)

    def show(self):
        print("show", self)

    def close(self):
        print("close", self)


if __name__ == '__main__':
    app = MyApplication()
    app.close()
