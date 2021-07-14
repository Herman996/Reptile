# encoding: utf-8

from multiprocessing import Process
from greenlet import greenlet
import time
from gevent import spawn


def read_book():
    for i in range(5):
        print('正在看书！！', i)
        g2.switch()


def listen_music():
    for i in range(5):
        print("正在听歌---->", i)
        g1.switch()

def read_book1():
    for i in range(5):
        print('正在看书！！', i)
        time.sleep(0.01)


def listen_music1():
    for i in range(5):
        print("正在听歌---->", i)
        time.sleep(0.01)


if __name__ == '__main__':
    g1 = greenlet(read_book)
    g2 = greenlet(listen_music)
    g1.switch()
    # g2.switch()