# encoding: utf-8
# 得到生成器的方式有：通过列表推导式、
"""
定义生成器的方式：
    1、通过列表推导式   g = (x + 1 for x in range(10))
    2、函数+yield
        def func():
            ....
            yield
        g = func()

生成器的方法：
    __next__()      获取到生成器中的值，没调用一次会产生一个新的元素，当元素产生完成后再次调用将会报错：StopIteration
    next()          同上
    sed(value)      向每次生成器调用中传值，第一次调用必须往里面传值None


生成器的应用： 协程
"""

list1 = [i*3 for i in range(10)]        # 列表推导式
g1 = (i*3 for i in range(3))           # 通过列表推导式得到的生成器

# print(next(g1))                         # 通过系统自带的next(生成器对象)，每调用一次生成一个新的元素
# print(next(g1))
# print(next(g1))
# print(next(g1))                         # 当通过next方法获取完所以到的元素后，再调用则会报错：StopIteration
while True:
    try:
        print(next(g1))
    except:
        print("元素导出完毕!!")
        break
# print(g1.__next__())                  # 通过__next__(),这个方法只在python3中有，在python2中没有

# 当函数中出现关键字yield，说明函数不是函数，是一个生成器，示例：
def test():
    n = 0
    while True:
        n += 1
        yield n     # 类似与return + 暂停的
test()           # 当函数为生成器时，在调用时需要使用变量接收
t = test()       # 得到的结果为生成器，在这里时不会执行函数
print(next(t))    # 通过next获取生成器中的元素，当获取生成器的元素时，才会执行函数test
print(next(t))    # 当第二次调用时，将会再次执行函数，while中的代码，可debug查看


def gen():
    i = 0
    while i < 5:
        temp = yield i
        print("temp:", temp)
        i += 1
    return "没有更多元素了"    # 在python2中会提示格式错误
g2 = gen()
# print(next(g2))
# print(next(g2))
# print(next(g2))
print(g2.send(None))        # sed为生成器的内置函数，可以调用生成器产生值

n1 = g2.send("呵呵")          # 这里是调用生成器时，替换里面的temp的值
print("n1:", n1)
n2 = g2.send("哈哈")
print("n2:", n2)


"""
可迭代的对象： 元组、列表、组合、字典、字符串
判断对象是否为可迭代的
from collections.abc import Iterable
print(isinstance(对象, Iterable))     # 返True表示对象为可迭代，False为不可迭代
可以被next()函数调用并不断返回在一个值的对象称为迭代器：Iterable
迭代器对象会从第一个元素开始访问，直到所有的元素被访问结束，不能回退
可以通过iter()函数将一个可迭代的变成一个迭代器
生成器是可迭代的，也是迭代器

生成器与迭代器的关系：
    
"""
from collections.abc import Iterable
list2 = [1, 2, 3]
f = isinstance(list2, Iterable)
print(f)




