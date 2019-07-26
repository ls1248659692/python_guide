#!/usr/bin/python
# coding=utf8

__author__ = 'Jam'
__date__ = '2019/7/4 9:12'

print('*1*'.center(50, '-'))


class Animal(object):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def print_weight(self):
        print("%s : %s" % (self.name, self.weight))


dog = Animal('hasky', 90)
dog.print_weight()
print(dog.weight)
dog.weight = 100
print(dog.weight)

print('*2*'.center(50, '-'))


class Animal(object):
    def __init__(self, name, weight):
        self.__name = name
        self.__weight = weight

    def print_weight(self):
        print("%s : %s" % (self.__name, self.__weight))

    def get_name(self):
        return self.__name

    def get_weight(self):
        return self.__weight

    def set_name(self, name):
        self.__name = name

    def set_weight(self, weight):
        self.__weight = weight


dog = Animal('hasky', 90)
print(dog.get_name())
dog.set_weight(100)
print(dog.get_weight())
print(dog.__dict__)

print('*3*'.center(50, '-'))


class Animal():
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def print_weight(self):
        print("%s : %s" % (self.name, self.weight))

    def run(self):
        print('Animal is running')


class Dog(Animal):
    def eat(self):
        print('Dog is eating')


a = Dog("hasky", 90)
b = Animal('tt', 10)
print(isinstance(a, Dog))
print(isinstance(a, Animal))
print(isinstance(b, Animal))
print(isinstance(b, Dog))

print('*4*'.center(50, '-'))


def run_twice(obj):
    obj.run()


a = Dog("hasky", 90)
b = Animal('tt', 10)
run_twice(a)
run_twice(b)

print('*5*'.center(50, '-'))


class Timer(object):
    def run(self):
        print('start....')


timer = Timer()
run_twice(timer)

print('*6*'.center(50, '-'))

print(dir('ABC'))
print('ABC'.__len__())
print(len('ABC'))

print('*7*'.center(50, '-'))


class Animal():
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def print_weight(self):
        print("%s : %s" % (self.name, self.weight))

    def run(self):
        print('Animal is running')


dog = Animal('hasky', 20)
print(hasattr(dog, 'name'))
setattr(dog, 'height', 20)
print(getattr(dog, 'height'))
print(getattr(dog, 'type', 'default'))
print('*8*'.center(50, '-'))

func = getattr(dog, 'run')
print(func, func())


class Animal():
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


dog = Animal('hasky', 90)
dog.height = 20
print(dog.height)

print('*9*'.center(50, '-'))


class Animal():
    tt = 'ss'

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


print(Animal.tt)
dog = Animal('hasky', 90)
print(dog.tt)
dog.tt = 'aa'
print(dog.tt)
print(Animal.tt)

print('*10*'.center(50, '-'))


class Animal():
    pass


ani = Animal()
ani.name = 'hasky'

from types import MethodType


def set_age(self, age):
    self.age = age


ani.set_age = MethodType(set_age, ani)
ani.set_age(20)
print(getattr(ani, 'age', 'default'))

print('*11*'.center(50, '-'))


class Animal(object):
    __slots__ = ['name', 'weight']


ani = Animal()
ani.name = 'hasky'
ani.weight = 90


# print(setattr(ani, 'age', 'default'))


class Dog(Animal):
    pass


dog = Dog()
dog.height = 20
print(dog.height)

print('*12*'.center(50, '-'))


class Animal(object):

    def get_weight(self):
        return self.weight

    def set_weight(self, value):
        if not isinstance(value, int):
            raise ValueError('weight must be an integer!')
        if not 0 <= value <= 200:
            raise ValueError('weight must between 1 ~ 200!')

        self.weight = value


ani = Animal()
ani.set_weight(60)
print(ani.get_weight())
ani.set_weight(200)

func = getattr(ani, 'set_weight')
print(func, func(1))
print(ani.set_weight(200))

print('*13*'.center(50, '-'))


class Animal(object):
    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        if not isinstance(value, int):
            raise ValueError('birth must be an integer!')
        if not 1 <= value <= 2018:
            raise ValueError('birth must between 1 ~ 2018!')
        self._birth = value

    @property
    def age(self):
        return 2018 - self._birth


ani = Animal()
ani.birth = 1958
print(ani.age)
print(ani.birth)

print('*14*'.center(50, '-'))


class Animal(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Animal object with name : %s' % self.name


print(Animal('tt'))
a = Animal('tt')
print(a)

print('*15*'.center(50, '-'))


class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        print(self.a, self.b)
        return self

    def next(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 10:
            raise StopIteration()
        return self.a


for n in Fib():
    print(n)

print('*16*'.center(50, '-'))


class Fib(object):
    def __getitem__(self, n):
        if isinstance(n, int):
            print(n)
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice):
            print(n)
            start = n.start
            stop = n.stop
            print(start, stop, n.step)
            if start is None:
                start = 0
            if stop is None:
                print('Max number should be 10')
                stop = 10 + 1

            a, b = 1, 1
            container = []
            for x in range(stop):
                if x >= start:
                    container.append(a)
                a, b = b, a + b
            return container


f = Fib()
print(range(0))
print(slice(1, 5))
print(f[0:11])
print(f[2:5])
print(f[:5])
print(f[1:])
print(f[10])

print('*17*'.center(50, '-'))


class Animal():
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __getattr__(self, attr):
        if attr == 'height':
            return 20


a = Animal("hasky", 90)
print(a.height)

print('*18*'.center(50, '-'))


class Animal():
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __getattr__(self, attr):
        if attr == 'height':
            return 178
        elif attr == 'age':
            return 18
        elif attr == 'function':
            return lambda: "function"
        raise AttributeError('Animal object has no attribute %s' % attr)


a = Animal("hasky", 90)
print(a.height)
print(a.age)
print(a.function())

print('*19*'.center(50, '-'))
