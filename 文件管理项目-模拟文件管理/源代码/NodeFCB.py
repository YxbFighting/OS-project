# -*- coding:utf-8 -*-
"""
Author :Yxxxb
Date   :2021/06/22
File   :NodeFCB.py
"""
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import re
from PIL import Image, ImageTk
import codecs
FileName = ""
varfile = ""
inichange = NONE

class NodeFCB:  # 目录节点
    def __init__(self, filename, iscont, tag):
        self.name = filename
        self.iscont = iscont
        self.tag = tag
        self.MDloc = 0
        self.status = 0
        self.linknum = 0
        self.endnum = 0
        # 位图 5*32*32
        # 模拟外存 5*1024
