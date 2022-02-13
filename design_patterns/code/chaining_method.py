class Player(object):
    def __init__(self, name):
        self.pos = (0, 0)

    def move(self, pos):
        self.pos = pos
        print("move to %s, %s" % self.pos)
        return self

    def say(self, text):
        print(text)
        return self

    def home(self):
        self.pos = (0, 0)
        print("I am home")
        return self


if __name__ == '__main__':
    p = Player('liuxin')
    p.move((1, 1)).say("haha").move((2, 3)).home().say("go to sleep")
