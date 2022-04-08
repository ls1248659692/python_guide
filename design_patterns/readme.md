Python Design Patterns
=======================


> "Design patterns help you learn from others’ successes instead of your own failures"

断断续续读了好久设计模式，记录此篇总结。设计模式最初发源于C++/Java等静态语言，Python语言本身的很多特性已经覆盖了设计模式，甚至用了都不知道，比如：decorator/metaclass/generator/getattr等。但是写稍微大型的项目时，还是经常力不从心。就如上面引用的那句话，通过设计模式可以学习前人的智慧，写出更好的代码。

python3环境下可以跑通，请跑起来玩玩。代码仅限演示作用，更注重清晰地用python语法展示patterns，而不是完备性，请勿用在生产环境。欢迎提issue和pr : )

## 设计模式六大原则


1. 单一职责原则
    * 一个类只做一件事情，模块化

1. 里氏替换原则
    * 所有使用父类的地方必须能完全替换为使用其子类
    * 即：子类可以扩展父类的功能，但不能改变父类原有的功能

1. 依赖倒置原则
    * 高层模块不应该依赖低层模块，二者都应该依赖其抽象
    * 抽象不应该依赖实现；实现应该依赖抽象
    * 面向接口编程，而不是面向实现编程，Duck Type

1. 接口隔离原则
    * 一个类对另一个类依赖的接口越少越好

1. 最小知识原则
    * 一个类对另一个类知道得越少越好

1. 开闭原则
    * 类、模块、函数对扩展开放，对修改关闭
    * 尽量在不修改源代码的情况下进行扩展


> 其实以上的原则不限于类的设计，很多工程上的系统设计也适用。


## 常用设计模式

### 创造模式
#### Singleton

一个类只有一个对象，似乎不太需要解释：）

```python
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
```

这个例子用MetaClass实现，其实Python里还有其他实现方式。但是Python里的MetaClass就是用来实例化Class的，用来实现单例类正好。


#### Factory

工厂模式，用于生产一大堆对象。这里用``__subclasses__``来获取子类，这样可以动态扩展子类而不改变factory的代码。
```python
class Shape(object):
    @classmethod
    def factory(cls, name, *args, **kwargs):
        types = {c.__name__: c for c in cls.__subclasses__()}  # 忽略性能:P
        shape_class = types[name]
        return shape_class(*args, **kwargs)


class Circle(Shape):
    pass


class Square(Shape):
    pass


if __name__ == '__main__':
    shapes = ["Circle", "Square", "Square", "Circle"]
    for i in shapes:
        s = Shape.factory(i)
        print(s)
```


### 结构模式

#### MVC
可能是最有名的设计模式，``数据<->控制器<->视图``。数据和视图分离，还可以同一份数据渲染多个视图。MVC做的最好的应该是各种Web框架和GUI框架。
```python
class Model(object):
    products = {
        'milk': {'price': 1.50, 'quantity': 10},
        'eggs': {'price': 0.20, 'quantity': 100},
        'cheese': {'price': 2.00, 'quantity': 10}
    }

    def get(self, name):
        return self.products.get(name)


class View(object):
    def show_item_list(self, item_list):
        print('-' * 20)
        for item in item_list:
            print("* Name: %s" % item)
        print('-' * 20)

    def show_item_info(self, name, item_info):
        print("Name: %s Price: %s Quantity: %s" % (name, item_info['price'], item_info['quantity']))
        print('-' * 20)

    def show_empty(self, name):
        print("Name: %s not found" % name)
        print('-' * 20)


class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self):
        items = self.model.products.keys()
        self.view.show_item_list(items)

    def show_item_info(self, item):
        item_info = self.model.get(item)
        if item_info:
            self.view.show_item_info(item, item_info)
        else:
            self.view.show_empty(item)


if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.show_items()
    controller.show_item_info('cheese')
    controller.show_item_info('apple')
```
上面的例子还只演示了数据到视图的渲染，其实MVC还包括通过视图修改数据。

#### Proxy
不直接调用一个类，而是通过一个代理来访问。这样做的好处有：可以切换底层实现、权限控制、安全检查等。当然最有用的是可以实现远程代理，jsonrpc就是一种。
```python
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
```

#### Decorator

装饰器，似乎不太需要解释，Python自带的语法，可以用来做很多事情，几个简单例子：

*   路由

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World'

@app.route('/home')
def home():
    return 'Welcome Home'
```

*   权限控制

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    ...
```

*   输入输出

```python
from functools import wraps


def debug(f):
    @wraps(f)
    def debug_function(*args, **kwargs):
        print('call: ', f.__name__, args, kwargs)
        ret = f(*args, **kwargs)
        print('return: ', ret)
    return debug_function


@debug
def foo(a, b, c=None):
    print(a, b, c)
    return True


if __name__ == '__main__':
    foo(1, 2, 3)
```




### 行为模式

#### Template

基类作为模板，定义好接口，子类来实现功能，最好的例子就是Qt里的各种QWidget。

```python
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
```

#### State Machine
状态机，`当前状态 + 操作 => 下一个状态`，似乎也不用怎么解释。如下例子实现的状态机，可以自定义状态、操作和转换规则。扩展的时候无需修改状态机代码，符合**开闭原则**。

```python
class StateMachine(object):

    def __init__(self, init_state):
        self.current_state = init_state
        self.current_state.run()

    def step(self, action):
        self.current_state = self.current_state.next(action)
        self.current_state.run()


class State(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<State '%s'>" % self.name

    def next(self, action):
        if (self, action) in mapping:
            next_state = mapping[(self, action)]
        else:
            next_state = self
        print("%s + %s => %s" % (self, action, next_state))
        return next_state

    def run(self):
        print(self, "is current state")


class Action(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<Action '%s'>" % self.name


State.Running = State("Running")
State.Stopped = State("Stopped")
State.Paused = State("Paused")

Action.start = Action("start")
Action.stop = Action("stop")
Action.pause = Action("pause")
Action.resume = Action("resume")


mapping = {
    (State.Stopped, Action.start): State.Running,
    (State.Running, Action.stop): State.Stopped,
    (State.Running, Action.pause): State.Paused,
    (State.Paused, Action.resume): State.Running,
    (State.Paused, Action.stop): State.Stopped,
}


if __name__ == '__main__':
    state_machine = StateMachine(State.Stopped)
    state_machine.step(Action.start)
    state_machine.step(Action.pause)
    state_machine.step(Action.resume)
    state_machine.step(Action.stop)
```

#### Iterator

迭代器，在Python中也不需要怎么解释，使用起来好像理所应当一样。实际上迭代器的一大优势是无需关心数据类型，一样的``for``语法。另一大优势是无需事先计算好所有元素，而是在迭代到的时候才计算。如下例子是Python中使用`yield`语法产生生成器`generator`来实现的迭代器，优势一目了然。
```python
def fibonacci(count=100):
    a, b = 1, 2
    yield a
    yield b
    while count:
        a, b = b, a + b
        count -= 1
        yield b


for i in fibonacci():
    print(i)
```

#### Command

Command封装了一个原子操作，在类外面实现，个人认为最大的作用是实现``redo/undo``。
```python
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
```

#### Chain Of Responsibility
链式Handler处理请求，某一个处理成功就返回。用Chain来动态构造Handler序列。
```python
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
```


#### Chaining Method

链式反应，就这样一直点下去。很多Query构造函数是这样，API更好用。

```python
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
```

#### Visitor
Visitor模式的目的是不改变原来的类，用另一个类来实现一些接口。下面的例子用Visitor模式实现了两种节点遍历的方法。
```python
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
```

#### Observer
当一个对象发生状态变化时，需要更新其他对象，用观察者模式来解耦这些对象，最小知识原则。
```python
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
```

上面的例子演示了最简单的实现，通常在实际程序中观察者模式会在不同线程中，要注意线程安全的问题。

## 参考链接
*   [python-patterns](https://github.com/faif/python-patterns)
*   [python-3-patterns-idioms](http://python-3-patterns-idioms-test.readthedocs.io/en/latest/index.html)
*   [设计模式六大原则](http://www.uml.org.cn/sjms/201211023.asp)
*   [设计模式一句话总结](https://zhuanlan.zhihu.com/p/28737945)
