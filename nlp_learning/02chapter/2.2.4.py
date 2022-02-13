# 列表常用方法
# list.append(x)    添加元素到列表尾部。
# list.extend(L)    列表合并。
# list.insert(i, x) 在指定位置插入一个元素。
# list.remove(x)    删除列表中值为 x 的第一个元素。
# list.pop([i])     从列表的指定位置删除元素，并将其返回。
# list.clear()      从列表中删除所有元素。相当于 del a[:]。
# list.index(x)     返回列表中第一个值为 x 的元素的索引。
# list.count(x)     返回 x 在列表中出现的次数。
# list.sort()       对列表中的元素就地进行排序。
# list.reverse()    就地倒排列表中的元素。
# list.copy()       返回列表的一个浅拷贝。等同于 a[:]。


# 列表的切分
def calllist(names):
    print(names[-1:]) # 输出列表最后一个值
    print(names[:3])  # 输出列表前3个值
calllist(names=['this','is','a','list'])


# 把列表当作堆栈使用
def SomeList(stack):
    print("原始列表（栈）：",end=' ')
    print(stack)
    stack.append('贺知章')
    stack.append('杜牧')
    print("追加后列表（栈）：",end=' ')
    print(stack)
    stack.pop()
    stack.pop()
    print("出栈后的数据：",end=' ')
    print(stack)

SomeList(stack=['李白','杜甫', '白居易'])

# 把列表当作队列使用：使用队列时调用collections.deque，它为在首尾两端快速插入和删除而设计。
from collections import deque
def SomeList2(queue):
    print("原始列表：",end=' ')
    print(queue)
    queue.append("李商隐")
    queue.append("杜牧")
    print("入队的列表：",end=' ')
    print(queue)
    queue.popleft()
    queue.popleft()
    print("出队后列表：",end=' ')
    print(queue)

SomeList2(queue = deque(['李白','杜甫', '白居易']))


# 列表推导式
def callList(nums):
    squares = [n**2 for n in nums]
    print(squares)
callList(nums=[2,4,6,8])


# 矩阵转秩
def countList(matrix):
    result = [[row[i] for row in matrix] for i in range(4)]
    print(result)

matrix = [
     [1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
]
countList(matrix)

