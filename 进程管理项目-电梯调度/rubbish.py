# -*- coding:utf-8 -*-
"""
Author :Yxxxb
Date   :2021/05/17
File   :rubbish.py
"""
# -*- coding:utf-8 -*-
"""
作者：叶冰冰冰冰
日期：2021年05月11日
"""
import threading, time
from time import ctime


class Elevator():
    def __init__(self, number):
        self.name = "Elevator" + str(number)
        self.status = 0
        self.power = 0
        self.floor = 1
        self.elevator_num = number
        self.door_open_button = 0
        self.warning_status = 0
        self.door_status = 0
        self.stop_times = 0
        self.work_time = 1
        self.target_status = 0  # 目标楼层乘客想去的方向 电梯上行接五楼的下行乘客 为-1


class GroupOfElevator(threading.Thread):  # 使用类定义thread，继承threading.Thread
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.args = args
        self.e1 = Elevator(1)
        self.e2 = Elevator(2)
        self.e3 = Elevator(3)
        self.e4 = Elevator(4)
        self.e5 = Elevator(5)
        self.ele_task = [[] for i in range(5)]  # 停车队列
        self.inside_task = [[] for i in range(5)]
        self.ele_group_task = [[0] * 20, [0] * 20]
        self.button_test = [[0] * 20, [0] * 20]
        self.ele = [self.e1, self.e2, self.e3, self.e4, self.e5]

    def warning(self):  # 外部调用
        pass

    def step(self):
        for e0 in self.ele:
            if e0.stop_times > 0:
                e0.stop_times -= 1
            else:
                if e0.status > 0:
                    e0.floor += 1
                elif e0.status < 0:
                    e0.floor -= 1

    def tell_inside_button(self, num, ele=Elevator):
        if num not in self.ele_task[ele.elevator_num - 1]:
            if num != ele.floor:
                if ele.status > 0 and num > ele.floor + 1:
                    self.ele_task[ele.elevator_num - 1].append(num)
                elif ele.status < 0 and num < ele.floor - 1:
                    self.ele_task[ele.elevator_num - 1].append(num)
                elif ele.status == 0 and num != ele.floor:
                    self.ele_task[ele.elevator_num - 1].append(num)
                return 0
        return 1

    def arrange1(self):
        for idxfloor, i in enumerate(self.ele_group_task[0]):
            if i == 1:
                min_working = 100
                min_static = 100
                min_working_index = -1
                min_static_index = -1
                tag = 4

                for idx, e0 in enumerate(self.ele):
                    if idxfloor + 1 in self.ele_task[idx]:
                        if self.button_test[0][idxfloor] == 1:
                            self.ele_group_task[1][idxfloor] = 0
                            return 1
                        else:
                            continue
                    if e0.status == 0:
                        if abs(e0.floor - (idxfloor + 1)) < min_static:
                            min_static = abs(e0.floor - idxfloor)
                            min_static_index = idx
                    elif e0.status == 1:
                        if e0.floor < idxfloor and (idxfloor - e0.floor) < min_working:
                            min_working = idxfloor - e0.floor
                            min_working_index = idx
                    else:
                        tag -= 1
                        continue
                if tag >= 0:
                    if min_working - 3 < min_static:
                        self.ele_task[min_working_index].append(idxfloor + 1)
                        self.ele[min_working_index].target_status = 1
                    else:
                        self.ele_task[min_static_index].append(idxfloor + 1)
                        self.ele[min_static_index].target_status = 1
                    self.ele_group_task[0][idxfloor] = 0

    def arrange2(self):
        for idxfloor, i in enumerate(reversed(self.ele_group_task[1])):
            if i == 1:
                min_working = 100
                min_static = 100
                min_working_index = -1
                min_static_index = -1
                tag = 4

                for idx, e0 in enumerate(self.ele):
                    if 19 - idxfloor + 1 in self.ele_task[idx]:
                        if e0.target_status == -1:
                            self.ele_group_task[1][19 - idxfloor] = 0
                            return 1
                        else:
                            continue
                    if e0.status == 0:
                        if abs(e0.floor - (19 - idxfloor + 1)) < min_static:
                            min_static = abs(e0.floor - 19 + idxfloor)
                            min_static_index = idx
                    elif e0.status == -1:
                        if e0.floor > 19 - idxfloor and (e0.floor - 19 + idxfloor) < min_working:
                            min_working = 19 - idxfloor - e0.floor
                            min_working_index = idx
                    elif e0.status == 1 and e0.target_status == -1:
                        if max(self.ele_task[idx]) > 20 - idxfloor:
                            tag = -1
                            break
                        if max(self.ele_task[idx]) <= 19 - idxfloor:
                            tag -= 1
                    else:
                        tag -= 1
                        continue
                if tag >= 0:
                    if min_working - 3 < min_static:
                        self.ele_task[min_working_index].append(19 - idxfloor + 1)
                        self.ele[min_working_index].target_status = -1
                    else:
                        self.ele_task[min_static_index].append(19 - idxfloor + 1)
                        self.ele[min_static_index].target_status = -1
                    self.ele_group_task[1][19 - idxfloor] = 0

    def schedule(self):
        for e0 in self.ele:
            while len(self.ele_task[e0.elevator_num - 1] or self.inside_task[e0.elevator_num - 1]) > 0:

                for i in self.inside_task[e0.elevator_num - 1]:
                    if self.tell_inside_button(i, e0):
                        self.inside_task[e0.elevator_num - 1] = []
                        return 1
                    self.tell_inside_button(i, e0)

                self.inside_task[e0.elevator_num - 1] = []

                self.ele_task[e0.elevator_num - 1].sort()

                if e0.floor > self.ele_task[e0.elevator_num - 1][0]:
                    self.ele_task[e0.elevator_num - 1] = self.ele_task[e0.elevator_num - 1][::-1]
                    e0.status = -1
                    e0.past_status = -1
                else:
                    e0.status = 1
                    e0.past_status = 1
                if e0.floor == self.ele_task[e0.elevator_num - 1][0]:
                    self.ele_task[e0.elevator_num - 1].pop(0)
                    e0.stop_times = 3
                if len(self.ele_task[e0.elevator_num - 1]) == 0:
                    e0.status = 0
                    e0.target_status = 0
                print(e0.name)
                print(e0.floor)
                print(ctime())
                print(self.ele_task[e0.elevator_num - 1])
                break

    def run(self, *args):  # run函数必须实现
        while 1:
            self.arrange1()
            self.schedule()
            self.arrange2()
            self.schedule()
            self.step()
            time.sleep(1)


def multithreading():
    # 创建线程
    e1 = GroupOfElevator(())
    e1.setDaemon(True)
    e1.start()

    e1.ele_group_task[0][5] = 1
    e1.ele_group_task[0][7] = 1
    time.sleep(2)
    e1.ele_group_task[0][3] = 1

    e1.join()

    print('end:%s' % ctime())


if __name__ == '__main__':
    # 启动线程
    # multithreading()

    s = [5, 3, 1]
    for i, j in enumerate(reversed(s)):
        print(i, j)


    def arrange1(self):
        for idxfloor, i in enumerate(self.ele_group_task[0]):
            if i == 1:
                min_working = 100
                min_static = 100
                min_working_index = -1
                min_static_index = -1
                tag = 4

                if self.button_test[0][idxfloor] == 1:
                    self.ele_group_task[1][idxfloor] = 0
                    return 1
                for idx, e0 in enumerate(self.ele):
                    if e0.status == 0:
                        if abs(e0.floor - (idxfloor + 1)) < min_static:
                            min_static = abs(e0.floor - idxfloor)
                            min_static_index = idx
                    elif e0.target_status != -1 and e0.status == 1:
                        if e0.floor < idxfloor and (idxfloor - e0.floor) < min_working:
                            min_working = idxfloor - e0.floor
                            min_working_index = idx
                    elif e0.status == -1 and e0.floor > idxfloor + 1:
                        if e0.target_status != -1 and min(self.ele_task[idx]) < idxfloor + 1:
                            tag = -1
                            break
                        else:
                            tag -= 1
                    else:
                        tag -= 1
                if tag >= 0:
                    if min_working - 3 < min_static:
                        self.ele_task[min_working_index].append(idxfloor + 1)
                        self.ele[min_working_index].target_status = 1
                    else:
                        self.ele_task[min_static_index].append(idxfloor + 1)
                        self.ele[min_static_index].target_status = 1
                    self.ele_group_task[0][idxfloor] = 0

                    elif e0.status == 1 and e0.floor < idxfloor + 5:
                        if e0.target_status != 1: # and max(self.ele_task[idx]) > idxfloor + 1:
                            tag = -1
                            break
                        else:
                            tag -= 1