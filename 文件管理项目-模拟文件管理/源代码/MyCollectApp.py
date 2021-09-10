# -*- coding:utf-8 -*-
"""
Author :Yxxxb
Date   :2021/06/22
File   :MyCollectApp.py
"""

from NodeFCB import *
from Content import *

class MyCollectApp(Toplevel):  # 重点
    def __init__(self):
        super().__init__()  # 重点
        self.title('用户信息')
        self.setupUI()

    def setupUI(self):
        row1 = Frame(self)
        row1.pack(side=TOP, fill=X)
        l1 = Label(row1, text="新建文件名与类型：", height=5, width=20)

        l1.pack(side=LEFT)  # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
        self.xls_text = StringVar()
        Button(row1, text="点击确认", command=self.on_click).pack(side=RIGHT)
        Entry(row1, textvariable=self.xls_text).pack(side=RIGHT)

        row2 = Frame(self)
        row2.pack(side=BOTTOM, fill="x")

        l = Label(row1, text="请输入文件名并选择新建文件类型", width=30, font=("楷体", 12))
        l.pack()

        varchoice = StringVar()
        r1 = Radiobutton(row1, text='目录/文件夹',
                         variable=varchoice, value='file', command=self.radioreturn1)
        r1.pack()
        r2 = Radiobutton(row1, text='.txt',
                         variable=varchoice, value='txt', command=self.radioreturn2)
        r2.pack()

    def radioreturn1(self):
        global varfile
        varfile = ""

    def radioreturn2(self):
        global varfile
        varfile = ".txt"

    def on_click(self):
        # print(self.xls_text.get().lstrip())
        global FileName
        FileName = self.xls_text.get().lstrip()
        if len(FileName) == 0:
            # print("用户名必须输入!")
            messagebox.showwarning(title='系统提示', message='请输入新建文件名!')
            return False
        self.quit()
        self.destroy()
        print("新建文件：%s" % (FileName))
