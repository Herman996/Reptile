# encoding: utf-8

import os
import hashlib
import base64
import random

import requests

"""
hashlib模块为加密算法    
    MD5算法运行1000次的平均时间为：226ms        
    SHA1算法运行1000次的平均时间为：308ms
    SHA256算法运行1000次的平均时间为：473ms
常见的为后面两种，md5为比较旧的加密方法，可通过撞库实现破解
目前的SSL证书必须使用SHA256加密方法
三种加密方法都是加密不可逆

"""
def sha():
    md5 = hashlib.md5()
    pwd = "123456"
    md5.update(pwd.encode("utf-8"))     # 在对传参进行加密的时候必须要加上encode指定编码
    print(md5.digest())             # 二进制的保存方法
    print(md5.hexdigest())          # 十六进制的保存方法，加密后的密文长度为32
    print(len(md5.hexdigest()))

    sha1 = hashlib.sha1(pwd.encode("utf-8"))        # 也可在创建加密对象时传递参数，传参时必须要通过encode指定编码
    print(sha1.hexdigest())        # 密文十六进制，加密后的密文长度为40
    print(sha1.digest())            # 密文二进制显示
    print(len(sha1.hexdigest()))

    sha256 = hashlib.sha256(pwd.encode("utf-8"))        # 同上，sha256加密示例
    print(sha256.hexdigest())           # 十六进制的加密密文长度为64
    print(sha256.digest())
    print(len(sha256.hexdigest()))


    # 使用base64进行加解密
    jm = base64.b64encode("hello world".encode("utf-8"))        # 对字符串hello world进行加密，通过encode指定编码
    xm = base64.b64decode(jm).decode("utf-8")                   # 对加密后的密文进行一个解密，通过decode指定解密后的编码
    print(jm)
    print(xm)

"""
进程
线程
协程

进程不能开太多，需要从cpu分类资源，进程的多少与服务器的硬件配置相关
"""
from multiprocessing import Process, Pool, Queue
import time
import os
"""
创建进程示例
    from multiprocessing import Process
    p = Process(target=callable, args=(c1, c2, c3, ), kwagrs='')
    p.start()       #  启动进程

主进程：执行的时候，默认的进程称为主进程
子进程：在主进程中可以开启子进程
进程中的全局变量，在每个子进程中都有一份全局变量，各自操作各自进程中的全局变量，子进程之间互不影响
阻塞主进程后面代码
    p1.join()   # p1为子进程对象
"""
number = 100
def program():
    global number
    for i in range(5):
        print("第{}行代码".format(i), os.getpid(), os.getppid())
        time.sleep(0.5)
    number -= 10
    print("program中的number：", number)

def listen_music():
    global number
    musics = ["《全球》", "《qq》", "《全球2》", "《全球3》"]
    for i in musics:
        print("正在听{}".format(i), os.getpid(), os.getppid())
        time.sleep(0.5)
    number -= 20
    print("listen_music中的number：", number)

def look_book(book):
    global number
    for i in range(5):
        print("正在看书《{}》的第{}页".format(book, i),os.getpid(), os.getppid())
        time.sleep(0.5)
    number -= 30
    print("look_book中的number：", number)

"""
进程池：
    Pool
    阻塞式：
    非阻塞式：
    
"""

def task1():
    print("this is task1", os.getpid(), os.getppid())
    return "task2"


def task2(msg):
    print("this is :", msg, os.getpid(), os.getppid())

# queue = Queue(3)
# queue.put("c1")
# queue.put("c2")
# queue.put("c3")
# print(queue.full())     # 判断队列是否满
# print(queue)
# # print(queue.qsize())    # 查看队列长度,在macos上无法运行，# Raises NotImplementedError on Mac OSX because of broken sem_getvalue()
# print(queue.get())      # 取出队列中的参数
# try:
#     queue.put("c4",timeout=3)
#     queue.put("c5", timeout=3)
# except:
#     print("队列阻塞，已满")
# while True:
#     try:
#         print(queue.get(timeout=1))
#     except:
#         print("队列为空，无参数")
#         break


def download_img(urls, queue):
    """
    用于下载图片
    :param urls:    王者荣耀英雄海报url列表
    :param queue:   这是一个queue对象
    :return:
    """
    for i in urls:
        response = requests.get(i)
        if response.status_code ==200:
            response = response.content
            try:
                queue.put(response, timeout=2)      # 设置写入超时时间为两秒，当写入失败表示队列满了
            except:
                print("写入队列超时，队列已满")
def save_img(queue):
    """
    此函数用于保存图片
    :param queue:   队列对象
    :return:
    """
    count = 0
    while True:
        try:
            data = queue.get(timeout=3)             # 取出队列中的值，超时时间为3秒，取出失败则表示队列中无值
            filename = 'img' + str(count) + '.jpg'
            with open(filename, 'wb') as img:
                img.write(data)
            count += 1
            print("图片{}保存完毕".format(filename))
        except:
            print("图片下载完毕！！")
            break


class DownloadProcess(Process):
    """
    重进程，创建一个新的进程类，继承Process
    """
    def __init__(self, queue, urls):
        """
        :param queue:   传递队列对象
        :param urls:    海报url列表
        """
        Process.__init__(self)  # 继承Process类中的__init__（即继承Process中所有的方法与变量）
        self.queue = queue
        self.urls = urls

    def run(self):
        """
        重写进程中的run函数，将run函数修改为下载图片
        :return:
        """
        for i in self.urls:
            response = requests.get(i)
            if response.status_code == 200:
                response = response.content
                try:
                    self.queue.put(response, timeout=2)
                    print("图片{}已下载完毕！！".format(i.split('/')[-1]))
                except:
                    print("写入队列超时，队列已满")

class Savefile_Process(Process):
    """
    同上
    """
    def __init__(self, queue):
        Process.__init__(self)
        self.queue = queue
    def run(self):
        """
        重构run函数的功能为保存图片
        :return:
        """
        count = 0
        while True:
            try:
                data = self.queue.get(timeout=3)
                filename = 'img' + str(count) + '.jpg'
                with open(filename, 'wb') as img:
                    img.write(data)
                count += 1
                print("图片{}保存完毕".format(filename))
            except:
                print("图片下载完毕！！")
                break

from threading import Thread, current_thread, Lock


def task3():
    for i in range(5):
        print("正在进行task3函数的第{}次任务".format(i), os.getpid(), os.getppid())
        time.sleep(0.5)

def task4(n):
    for i in range(n):
        print("正在进行task4函数的第{}次任务".format(i), os.getpid(), os.getppid())
        time.sleep(0.5)

class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    def run(self):
        for i in range(5):
            print("正在进行自定义线程中的第{}次任务".format(i), os.getpid(), os.getppid())
            time.sleep(0.5)

ticket = 10

def sale_ticket(lock):
    global ticket
    while True:
        lock.acquire(1)
        if ticket > 0:
            print("{}正在出售第{}张票".format(current_thread().name, ticket))
            ticket -= 1
            lock.release()
            time.sleep(0.5)
        else:
            print("{}提示：票卖完了！！".format(current_thread().name))
            lock.release()
            break

n = 0
def error_task():
    global n
    for i in range(100000):
        n +=1

def task5(lock):
    global n
    lock.acquire()          # 握住锁
    for i in range(100000):
        n +=1
    lock.release()          # 释放锁

def task6(lock1, lock2):
    if lock1.acquire():
        print("{}获取到lock1锁！！".format(current_thread().name))
        for i in range(5):
            print('{}----->'.format(current_thread().name), i)
            time.sleep(0.01)
        if lock2.acquire(timeout=2):
            print("{}获取到lock2锁！！".format(current_thread().name))
            lock2.release()
        lock1.release()

def task7(lock1, lock2):
    if lock2.acquire():
        print("{}获取到lock2锁！！".format(current_thread().name))
        for i in range(5):
            print('{}----->'.format(current_thread().name), i)
            time.sleep(0.01)
        if lock1.acquire(timeout=2):
            print("{}获取到lock1锁！！".format(current_thread().name))
            lock1.release()
        lock2.release()

def producer(queue):
    print("{}起床了".format(current_thread().name))
    books = ["三国演义", "水浒传", "红楼梦", "西游记"]
    for i in range(10):
        book = random.choice(books)
        print("{}正在加载中......".format(book))
        time.sleep(1)
        print("已加载完毕！！！")
        queue.put(book)
    queue.put(None)
def consumer(queue):
    print("{}准备看书".format(current_thread().name))
    while True:
        book = queue.get()
        if book:
            print("正在看{}".format(book))
        else:
            print("名著已看完")
            break

if __name__ == '__main__':
    print("当前py文件进程号{} 以及父进程号{}".format(os.getpid(), os.getppid()))
    # p1 = Process(target=program)            # 通过Process创建一个进程对象
    # p2 = Process(target=listen_music)
    # p3 = Process(target=look_book, args=("西游记", ))      # 在创建一个进程时指定执行的函数，并传递参数
    # p1.start()
    # p2.start()
    # p3.start()
    # # p1.run()      # 使用run时仅仅是运行这个进程，并且是串行，不会去cpu中分配新的资源
    # # p2.run()
    # # p3.run()
    # # p1.terminate()        # 终止进程，进程未执行完也终止，但是不释放进程占用的资源
    # # print(p1.is_alive())         # 判断进程是否存活,True为存活，False为结束
    # # join()    加入，阻塞主进程后面的代码不执行,当对应的子进程执行完成后再执行
    # p1.join()
    # p2.join()
    # p3.join()
    # print("main中的number：", number)
    # # p1.close()                # 用于释放进程占用的资源，当进程在运行是，不可释放，将会报错，可以与terminate配合使用
    # # p2.close()
    # pool = Pool(4)      # 创建进程池
    # # 非阻塞式
    # for i in range(10):
    #     pool.apply_async(task1, callback=task2)     # 阻塞式：进程池中一个任务结束后才能进行下一个任务
    #     print("------------------------>", i)
    # pool.close()
    # pool.join()             # 阻塞进程池,只有执行完一个进程才会执行下一个,执行完进程池中的所有进程才会执行主进程后面的代码
    # print("main, over")
    # urls = [
    #     "http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/538/538-bigskin-1.jpg",
    #     "http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/528/528-bigskin-1.jpg",
    #     "http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/137/137-bigskin-1.jpg"
    # ]
    # queue = Queue(3)
    # p1 = Process(target=download_img, args=(urls, queue, ))
    # p2 = Process(target=save_img, args=(queue, ))
    # star_time = time.time()
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # end_time = time.time()
    # print("下载图片用时{}秒".format(end_time - star_time))
    # dprocess = DownloadProcess(queue, urls)
    # sprocess = Savefile_Process(queue)
    # star_time = time.time()
    # dprocess.start()
    # sprocess.start()
    # dprocess.join()
    # sprocess.join()
    # end_time = time.time()
    # print("下载图片用时{}秒".format(end_time - star_time))


    # 线程的用法
    # t3 = Thread(target=task3, name="task3")               # 创建线程对象，name配置线程名
    # t4 = Thread(target=task4, args=(6, ))
    # t5 = MyThread(name="自定义线程")                     # 创建自定义线程对象并指定线程名
    # t5.start()                          # 启动自定义线程对象
    # t5.join()
    # print("t5线程名：:",t5.name)                      # 查看当前线程名
    # print(t3.isDaemon())    # 判断
    # t3.start()              # 启动线程
    # t4.start()
    # print(t3.is_alive())           # 判断线程是否存活
    # print(t3.is_alive())
    # t4.join()
    # t3.join()               # 阻塞线程
    # print(t3.isDaemon())
    # t6 = Thread(target=sale_ticket, name="一号窗口")            # 创建线程对象，并指定线程名
    # t7 = Thread(target=sale_ticket, name="二号窗口")
    # t8 = Thread(target=sale_ticket, name="三号窗口")
    # t9 = Thread(target=sale_ticket, name="四号窗口")
    # t10 = Thread(target=sale_ticket, name="五号窗口")
    # t6.start()                              # 启动线程
    # t7.start()
    # t8.start()
    # t9.start()
    # t10.start()
    # n1 = Thread(target=error_task, name='task1')
    # n2 = Thread(target=error_task, name='task2')
    # n3 = Thread(target=error_task, name='task3')
    # n1.start()
    # n2.start()
    # n3.start()
    # n1.join()
    # n2.join()
    # n3.join()
    # print(n)            # 这就可能造成数据不准
    lock = Lock()
    # s1 = Thread(target=task5, name='task1', args=(lock, ))
    # s2 = Thread(target=task5, name='task2', args=(lock, ))
    # s3 = Thread(target=task5, name='task3', args=(lock, ))
    # s1.start()
    # s2.start()
    # s3.start()
    # s1.join()
    # s2.join()
    # s3.join()
    # print(n)            # 正常
    # t6 = Thread(target=sale_ticket, name="一号窗口", args=(lock, ))            # 创建线程对象，并指定线程名
    # t7 = Thread(target=sale_ticket, name="二号窗口", args=(lock, ))
    # t8 = Thread(target=sale_ticket, name="三号窗口", args=(lock, ))
    # t9 = Thread(target=sale_ticket, name="四号窗口", args=(lock, ))
    # t10 = Thread(target=sale_ticket, name="五号窗口", args=(lock, ))
    # t6.start()                              # 启动线程
    # t7.start()
    # t8.start()
    # t9.start()
    # t10.start()

    # 死锁
    # lock1 = Lock()
    # lock2 = Lock()
    # t1 = Thread(target=task6, args=(lock1, lock2, ))
    # t2 = Thread(target=task7, args=(lock1, lock2,))
    # t1.start()
    # t2.start()

    # 线程间消费
    queue = Queue(2)
    t1 = Thread(target=producer, name="看书", args=(queue, ))
    t2 = Thread(target=consumer, name = "张三", args=(queue, ))
    t1.start()
    t2.start()