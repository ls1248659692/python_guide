class Shape(object):
    @classmethod
    def factory(cls, name, *args, **kwargs):
        types = {c.__name__: c for c in cls.__subclasses__()}
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
