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
