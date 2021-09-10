# -*- coding: utf-8 -*-
"""
Author :Yxxxb
Date   :2021/06/19
File   :操作系统文件管理
"""
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import re
from PIL import Image, ImageTk
import codecs

a = ["0", "00", "01", "02", "03", "000", "001", "002", "003"]
FileName = ""
varfile = ""
inichange = NONE


class NodeFCB:  # 目录节点
    def __init__(self, filename, iscont, tag):
        self.name = filename
        self.iscont = iscont
        self.tag = tag
        self.MDloc = 0
        # 位图 5*32*32
        # 模拟外存 5*1024


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


class Application_UI(object):
    # path = r"E:\\python开发工具\\project\\tkinter"
    path = os.path.abspath(".")
    file_types = [".png", ".jpg", ".jpeg", ".ico", ".gif"]
    scroll_visiblity = True

    font = 11
    font_type = "Courier New"

    def __init__(self):

        self.content = Content()
        for i in self.content.contlist:
            print(str(i.name[0]))
        print("input over")
        self.sumMD = 10000
        self.eachMD = 5
        self.bitmap = [2000]  # 0无 -1尾

        # 设置UI界面
        window = Tk()
        self.root = window
        win_width = 800
        win_height = 450

        screen_width, screen_height = window.maxsize()
        x = int((screen_width - win_width) / 2)
        y = int((screen_height - win_height) / 2)
        window.title("MyFileManagement")
        window.geometry("%sx%s+%s+%s" % (win_width, win_height, x, y))

        menu = Menu(window)
        window.config(menu=menu)

        selct_path = Menu(menu, tearoff=0)
        selct_path.add_command(label="打开", accelerator="Ctrl + O", command=self.open_dir)
        selct_path.add_command(label="保存", accelerator="Ctrl + S", command=self.save_file)

        menu.add_cascade(label="文件", menu=selct_path)

        about = Menu(menu, tearoff=0)
        about.add_command(label="版本", accelerator="操作系统文件管理")
        about.add_command(label="作者", accelerator="1953348 叶栩冰")
        menu.add_cascade(label="关于", menu=about)

        # 顶部frame
        top_frame = Frame(window, bg="#fff")
        top_frame.pack(side=TOP, fill=X)
        label = Label(top_frame, text="请您点击文件右键选择修改进行文件读写", bg="#fff")
        label.pack(side=LEFT)

        self.path_var = StringVar()
        self.path_var.set("")
        label_path = Label(top_frame, textvariable=self.path_var, bg="#fff", fg="red", height=2)
        label_path.pack(side=LEFT)
        lbtitle = Label(top_frame, text='操作系统第三次课程作业 文件管理项目      ', fg="black", bg="white",
                        font=("楷体", 18))
        lbtitle.pack(side=RIGHT)

        paned_window = PanedWindow(window, showhandle=True, orient=HORIZONTAL)
        paned_window.pack(expand=1, fill=BOTH)

        # 左侧frame
        self.left_frame = Frame(paned_window)
        paned_window.add(self.left_frame)

        # lb1 = Button(self.left_frame, text='frm1', command=self.deleteme)
        # lb1.pack()

        # 鼠标
        menu = Menu(self.left_frame, tearoff=0)
        menu.add_command(label="新建文件", command=self.newfile)
        menu.add_command(label="删除文件", command=self.deleteme)
        menu.add_command(label="格式化磁盘", command=self.format)
        menu.add_command(label="查看修改文件", command=self.showf)

        def popupmenu(event):
            menu.post(event.x_root, event.y_root)

        window.bind("<Button-3>", popupmenu)

        self.tree = ttk.Treeview(self.left_frame, show="tree", selectmode="browse")
        tree_y_scroll_bar = Scrollbar(self.left_frame, command=self.tree.yview, relief=SUNKEN, width=2)
        tree_y_scroll_bar.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=tree_y_scroll_bar.set)
        self.tree.pack(expand=1, fill=BOTH)

        # 右侧frame
        self.right_frame = Frame(paned_window)
        paned_window.add(self.right_frame)

        # enterfile=Entry(self.right_frame, highlightcolor='red', highlightthickness=1)
        # enterfile.place(x=10,y=10,width=300, height=150)
        # enterfile.pack(side = LEFT, fill = BOTH)

        textlb = Label(self.right_frame, text='=============================================\n'
                                              '请您在窗口左侧的文件树处选中想要处理文件\n'
                                              '请您右键所选中的文件来选择对该文件的操作\n'
                                              '由于需要维护磁盘，您不可删除此电脑与本地磁盘\n'
                                              '同理您也无法在与此电脑同级位置建立目录或文件\n'
                                              '选中文件进行修改后请点击保存按钮更新文件内容\n'
                                              '=============================================', fg="black", bg="white",
                       font=("楷体", 12))
        textlb.pack(side=TOP)

        self.w1 = Text(self.right_frame, width=60, height=12, bg="white", font=("楷体", 12))
        self.w1.pack()

        self.b1 = Button(self.right_frame, text="保存", command=self.saveText, activebackground='gray', bd=5,
                         font=('楷体', 15))
        self.b1.pack()
        self.block_var = StringVar()
        self.block_var.set("")
        textlc = Label(self.right_frame, text='模拟内存：40KB 模拟磁盘盘块大小：4B', fg="black", bg="white",
                       font=("楷体", 12))
        textlc.pack(side=LEFT)

        # 右下角frame

        self.folder_img = PhotoImage(file=r"./image/folder.png")
        self.file_img = PhotoImage(file=r"./image/text_file.png")

        php_img = PhotoImage(file=r"./image/php.png")
        python_img = PhotoImage(file=r"./image/python.png")
        image_img = PhotoImage(file=r"./image/img.png")
        txt_img = PhotoImage(file=r"./image/text_file.png")

        # 设置文件图标
        self.icon = {".php": php_img, ".py": python_img, ".pyc": python_img, ".png": image_img, ".jpg": image_img,
                     ".jpeg": image_img, ".gif": image_img, ".ico": image_img}

        # 加载目录文件  root, filelist, filename, depth

        self.load_self_tree("", self.content.contlist, self.content.contlist[0].name[0], "0", 1)
        print(self.path)
        """
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.select_tree())

        text.bind("<MouseWheel>", lambda event: self.update_line())
        
        self.number_line.bind('<Button-3>', self.mouse_reght)
        self.number_line.bind("<FocusIn>", self.focus_in_event)
        self.number_line.bind('<Button-1>', self.button_ignore)
        self.number_line.bind('<Button-2>', self.button_ignore)
        self.number_line.bind('<Button-3>', self.button_ignore)
        self.number_line.bind('<B1-Motion>', self.button_ignore)
        self.number_line.bind('<B2-Motion>', self.button_ignore)
        self.number_line.bind('<B3-Motion>', self.button_ignore)

        self.text_scroll_obj.bind('<B1-Motion>', lambda event: self.update_line())
        self.text_obj.bind('<KeyRelease>', lambda event: self.update_line())

        text.bind("<Control-Key-s>", lambda event: self.save_file())
        text.bind("<Control-Key-S>", lambda event: self.save_file())
        text.bind("<Control-Key-Z>", lambda event: self.toUndo())
        text.bind("<Control-Key-Y>", lambda event: self.toRedo())
        """
        print(a)
        window.mainloop()

    def deleteme(self):
        print("deletefile")
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            print(item_text)
            if item_text[0] == '0' or item_text[0] == '00':
                messagebox.showwarning('Warning', '由于需要保障系统安全性\n您不可以删除此电脑或本地磁盘C！')
                return 0
            self.tree.delete(item)
            for i in self.content.contlist:
                print(i.tag[0], i.name[0])
            print("*****")
            j = 100
            while j > 0:
                for index, file in enumerate(self.content.contlist):
                    if file.tag[0] == item_text[0] or file.tag[0][0:len(item_text[0])] == item_text[0]:
                        self.content.contlist.pop(index)
                        break
                j -= 1
            for i in self.content.contlist:
                print(str(i.name[0]))
        self.writefile()

    def newfile(self):
        print("newfile")
        print(a)
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            print(item_text)
            if item_text[0] == '0':
                messagebox.showwarning('Warning', '注意新建文件位置！\n请在此电脑根目录下建立文件！')
                return 0
            min = '0'
            num = 0

            app = MyCollectApp()
            app.mainloop()
            global varfile, FileName

            for subitem in self.tree.get_children(self.tree.parent(item)):
                print(self.tree.item(subitem, "values"))
                if min < subitem[-1]:
                    min = subitem[-1]
                    num += 1
            filetag = self.tree.item(self.tree.parent(item), "values")[0]
            filetag = filetag[0:num] + str(num)
            filename = FileName + varfile

            for node in self.content.contlist:
                if len(node.tag[0]) == len(filetag) and (
                        node.name[0] == FileName or node.name[0] == FileName + '.txt') and node.tag[0][0:len(
                    node.tag[0]) - 1] == filetag[0:len(node.tag[0]) - 1]:
                    messagebox.showwarning('Warning', '新建文件不可与该根目录下文件重名！')
                    return 0

            lisroot = "1"
            if varfile == "":
                self.tree.insert(self.tree.parent(item), END, text=" " + filename, open=1, values=filetag
                                 , image=self.folder_img)
                lisroot = "1"
            else:
                self.tree.insert(self.tree.parent(item), END, text=" " + filename, open=1, values=filetag
                                 , image=self.file_img)
                lisroot = "0"
                file = open("./EM/EM.txt", "a+", encoding='utf-8')
                content = 'FILENAMEIS ' + str(filetag)
                file.write(content)
                file.close()
            addnode = NodeFCB([str(filename)], [str(lisroot)], [str(filetag)])
            addnode.iscont = lisroot
            print(addnode.name)
            self.content.contlist.append(addnode)
            for i in self.content.contlist:
                print(i.tag[0], i.name[0])
            self.writefile()

    def format(self):
        print("*")
        self.content.contlist = self.content.contlist[0:2]
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)
        file = open("./memory.txt", "w", encoding='utf-8')
        content = '0 此电脑 1\n00 本地磁盘C 1'
        file.write(content)
        file.close()
        self.load_self_tree("", self.content.contlist, self.content.contlist[0].name[0], "0", 1)

    def saveText(self):
        # INSERT  表示在光标处插入 self.w1.insert(END, "rrrr")
        result = self.w1.get("1.0", "end")  # 获取文本框输入的内容
        print(result)
        print(len(str(result)))

        file = open("./EM/EM.txt", "r", encoding='utf-8')
        content = file.read()
        global inichange
        name = inichange
        filename = 'FILENAMEIS ' + name
        pos = content.find(filename)
        addcontent = '\n' + result
        elsefile = content[pos + len(filename):]
        len1 = len('FILENAMEIS ')
        pl = 0
        for each in range(len(elsefile) - len1):
            if elsefile[each:each + len1] == 'FILENAMEIS ':  # 找出与子字符串首字符相同的字符位置
                pl = each
                break
        elsefile = elsefile[pl:]

        if pos != -1:
            content = content[:pos + len(filename)] + addcontent + elsefile

        file = open("./EM/EM.txt", "w", encoding='utf-8')
        file.write(content)
        file.close()

    def showf(self):
        print("showfile")
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            print(item_text)
            global inichange
            inichange = item_text[0]
            for node in self.content.contlist:
                if node.tag[0] == item_text[0]:
                    if node.iscont[0] == '1':
                        messagebox.showwarning('Warning', '您仅可以查看文件信息！')
                        return 0

            file = open("./EM/EM.txt", "r", encoding='utf-8')
            content = file.read()
            filename = 'FILENAMEIS ' + item_text[0]

            pos = content.find(filename)

            elsefile = content[pos + len(filename):]

            len1 = len('FILENAMEIS ')
            pl = 0
            for each in range(len(elsefile) - len1):
                if elsefile[each:each + len1] == 'FILENAMEIS ':  # 找出与子字符串首字符相同的字符位置
                    pl = each
                    break
            elsefile = elsefile[1:pl - 1]
            print(elsefile)
            self.w1.delete('1.0', 'end')
            self.w1.insert(END, elsefile)

            file.close()

    def writefile(self):
        f = codecs.open('memory.txt', mode='w', encoding='utf-8')  # 打开txt文件，以‘utf-8’编码读取

        for i in self.content.contlist:
            f.write(str(i.tag[0]) + " " + str(i.name[0]) + " " + str(i.iscont[0]) + "\n")

        f.close()


class Application(Application_UI):
    def __init__(self):
        Application_UI.__init__(self)

    ''' 保存文件'''

    def save_file(self):
        # 判断是否是文件
        path = self.path_var.get()
        print(path)
        if self.is_file(path) is True:
            # 判断是否为图片
            if self.is_type_in(path) is False:
                content = self.text_obj.get(1.0, END)[:-1]
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("提示", "保存成功")
            else:
                messagebox.showwarning("提示", "不能保存图片")
        else:
            messagebox.showwarning("提示", "不能保存目录")

    ''' 设置默认搜索路径'''

    def open_dir(self):
        path = filedialog.askdirectory(title=u"设置目录", initialdir=self.path)
        print("设置路径：" + path)
        self.path = path
        # 删除所有目录
        self.delete_tree()
        self.load_tree("", self.path)

    ''' 判断是否为文件'''

    def is_file(self, path):
        if os.path.isfile(path):
            return True
        return False

    ''' 判断是否是图片类型'''

    def is_type_in(self, path):
        ext = self.file_extension(path)
        if ext in self.file_types:
            return True
        return False

    ''' 删除树'''

    def delete_tree(self):
        self.tree.delete(self.tree.get_children())

    def focus_in_event(self, event=None):
        self.text_obj.focus_set()

    def button_ignore(self, ev=None):
        return "break"

    ''' 加载目录'''

    def load_self_tree(self, root, filelist, filename, filetag, depth):
        is_open = False
        if root == "":
            is_open = True
        tag = 0
        for file in filelist:
            exists = (file.tag[0][0:depth] == filetag and len(file.tag[0]) == 1 + len(filetag))
            if exists:
                tag = 1
                break
        print(tag)
        print(filename)
        print(filetag)
        if tag:
            root = self.tree.insert(root, END, text=" " + filename, open=is_open, values=filetag
                                    , image=self.folder_img)
        else:
            root = self.tree.insert(root, END, text=" " + filename, open=is_open, values=filetag
                                    , image=self.file_img)

        for file in filelist:
            exists = (file.tag[0][0:depth] == filetag and len(file.tag[0]) == 1 + len(filetag))

            if exists:
                self.load_self_tree(root, filelist, file.name[0], file.tag[0], depth + 1)
            else:
                continue

    def load_tree(self, root, path):
        is_open = False
        if root == "":
            is_open = True

        root = self.tree.insert(root, END, text=" " + self.dir_name(path), values=(path,), open=is_open,
                                image=self.folder_img)

        try:
            for file in os.listdir(path):
                file_path = path + "\\" + file
                if os.path.isdir(file_path):
                    self.load_tree(root, file_path)
                else:
                    ext = self.file_extension(file)
                    img = self.icon.get(ext)
                    if img is None:
                        img = self.file_img
                    self.tree.insert(root, END, text=" " + file, values=(file_path,), image=img)
        except Exception as e:
            print(e)

    ''' 获取文件后缀'''

    def file_extension(self, file):
        file_info = os.path.splitext(file)
        return file_info[-1]

    ''' 获取目录名称'''

    def dir_name(self, path):
        path_list = os.path.split(path)
        return path_list[-1]

    ''' 更新行数'''

    def update_line(self):
        if not self.scroll_visiblity:
            return
        self.number_line.delete(1.0, END)
        text_h, text_l = map(int, str.split(self.text_obj.index(END), "."))
        q = range(1, text_h)
        r = map(lambda x: '%i' % x, q)
        s = '\n'.join(r)
        self.number_line.insert(END, s)

        if text_h <= 100:
            width = 2
        elif text_h <= 1000:
            width = 3
        elif text_h <= 10000:
            width = 4
        else:
            width = 5
        self.number_line.configure(width=width)
        self.number_line.yview_moveto(self.text_obj.yview()[0])

    ''' 选中item回调

    def select_tree(self):
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            select_path = "\\".join(item_text)
            self.path_var.set(select_path)

            self.text_obj.config(state=NORMAL, cursor="xterm")
            # 清空text内容
            self.text_obj.delete(1.0, END)
            self.update_line()
            if self.is_file(select_path) is True:
                if self.is_type_in(select_path) is True:
                    self.text_obj.config(state=DISABLED, cursor="")
                    self.look_image(select_path)
                else:
                    try:
                        self.open_file(select_path, "r", "utf-8")
                        self.update_line()
                    except Exception as e:
                        print(e)
            else:
                self.text_obj.config(state=DISABLED, cursor="")'''

    ''' 查看图片'''

    def look_image(self, select_path):
        try:
            image = Image.open(select_path)
            self.look_photo = ImageTk.PhotoImage(image)
            self.text_obj.image_create(END, image=self.look_photo)
        except Exception as e:
            print(e)

    ''' 打开文件写入内容'''

    def open_file(self, select_path, mode, encoding=None):
        with open(select_path, mode=mode, encoding=encoding) as f:
            self.text_obj.insert(1.0, f.read())


if __name__ == "__main__":
    Application()
