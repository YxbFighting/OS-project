# -*- coding:utf-8 -*-
"""
Author :Yxxxb
Date   :2021/06/22
File   :Content.py
"""
from NodeFCB import *

class Content:  # 读存储目录 修改目录
    def __init__(self):
        self.contlist = []
        self.readfile()

    def readfile(self):
        f = codecs.open('memory.txt', mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8’编码读取
        line = f.readline()  # 以行的形式进行读取文件
        while line:
            a = line.split()
            ltag = a[0:1]
            lname = a[1:2]
            lisRoot = a[2:3]
            node = NodeFCB(lname, lisRoot, ltag)
            self.contlist.append(node)
            line = f.readline()

        f.close()
