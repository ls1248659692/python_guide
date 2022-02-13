# 输出指定数的斐波那契数列
def fib(n):
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()
fib(100)

# 函数默认参数
def sayhello(name="Tom"):
    print("Hello,"+name)

sayhello()

# 关键字参数
def person(name, age, **kw):  #前两个是必须参数，最后一个可选可变参数
    print('name:', name, 'age:', age, 'other:', kw)

person("Tome",30) # 只调用必须参数
person("Tom",30,city="ChengDu",sex="man") # 自定义关键字参数

# 可变参数
def concat(*args, sep="/"):
    print(sep.join(args))
concat('我','是','可变','参数')

# Lambda 形式
def Lambda(nums):
    nums.sort(key=lambda num: num[0])
    print(nums)

Lambda(nums = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')])
