# !/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
from tkFont import Font
from tkMessageBox import *
import json
from functions import load_config

import ttk

try:
    from ttk import Entry, Button
except ImportError:
    pass

config_path = "config.json"


class Login(object):

    def __init__(self):
        self.root = Tk()
        self.root.title(u'武汉大学图书馆座位预约系统')
        self.root.resizable(True, True)
        self.root.geometry('+450+250')
        # self.root.geometry('350x150')

        self.sysfont = Font(self.root, size=14)

        self.lb_user = Label(self.root, text=u'学号:', padx=8, pady=10)
        self.lb_passwd = Label(self.root, text=u'密码:', padx=8)
        self.lb_user.grid(row=0, column=0, sticky=W)
        self.lb_passwd.grid(row=1, column=0, sticky=W)

        self.en_user = Entry(self.root, font=self.sysfont, width=22)
        self.en_passwd = Entry(self.root, font=self.sysfont, width=22)
        self.en_user.grid(row=0, column=1, columnspan=2, padx=2)
        self.en_passwd.grid(row=1, column=1, columnspan=2, padx=2)

        # self.en_user.insert(0, u'输入学号')
        # self.en_passwd.insert(0, u'输入密码')

        # 从config.json中读取用户名和密码
        self.en_user.insert(0, self.load_config_before()["username"])
        self.en_passwd.insert(0, self.load_config_before()["password"])
        # 隐藏密码
        self.en_passwd.config(show='*')

        self.en_user.config(validate='focusin',
                            validatecommand=lambda: self.validate_func('self.en_user'),
                            invalidcommand=lambda: self.invalid_func('self.en_user'))
        self.en_passwd.config(validate='focusin',
                              validatecommand=lambda: self.validate_func('self.en_passwd'),
                              invalidcommand=lambda: self.invalid_func('self.en_passwd'))
        # 记住密码checkbox
        self.var = IntVar()
        self.ckb_remember = Checkbutton(self.root, text=u'记住密码', underline=0, variable=self.var)
        self.ckb_remember.grid(row=3, column=0)

        # 启用邮件通知checkbutton
        self.var = IntVar()
        self.ckb = Checkbutton(self.root, text=u'启用邮件通知', underline=0, variable=self.var)
        self.ckb.grid(row=3, column=1)

        # 确定按钮
        self.bt_print = Button(self.root, text=u'确定')
        self.bt_print.grid(row=3, column=2, pady=3)
        self.bt_print.config(command=self.send_info)

        self.root.bind('<Return>', self.enter_print)

        # 创建所选座位号label
        # self.seat_text = str(self.load_config_before()["seats"])
        # self.label_seat = ttk.Label(self.root, text=self.seat_text, relief=RIDGE).grid(row=3, column=0)

        # 创建一个日期下拉列表
        self.date = StringVar()
        self.date_chosen = ttk.Combobox(self.root, width=5, textvariable=self.date)
        self.date_chosen['values'] = ("today", "tomorrow")  # 设置下拉列表的值
        self.date_chosen.grid(column=0, row=2, pady=8, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.date_chosen.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 创建一个起始时间下拉列表
        self.startTime = StringVar()
        self.startTime_chosen = ttk.Combobox(self.root, width=7, textvariable=self.startTime)
        self.startTime_chosen['values'] = ("480", "510", "540", "570", "600", "630", "660", "690", "720")  # 设置下拉列表的值
        self.startTime_chosen.grid(column=1, row=2, padx=10)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.startTime_chosen.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 创建一个终止时间下拉列表
        self.endTime = StringVar()
        self.endTime_chosen = ttk.Combobox(self.root, width=7, textvariable=self.endTime)
        self.endTime_chosen['values'] = ("480", "510", "540", "570", "600", "630", "660", "690", "720")  # 设置下拉列表的值
        self.endTime_chosen.grid(column=2, row=2)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.endTime_chosen.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 创建信息栏
        self.info = Text(self.root, height=8, width=30)
        # self.info.pack(side=RIGHT, fill=Y)
        self.info.grid(column=3, row=0, rowspan=4, padx=5)
        self.info.insert(END, "runtime info:")


        self.root.mainloop()

    def load_config_before(self):
        """从config.json中读取原来的配置"""
        return load_config()

    def validate_func(self, en):
        """验证输入"""
        return False if eval(en).get().strip() != '' else True

    def invalid_func(self, en):
        """表面"""
        value = eval(en).get().strip()
        if value == u'输入学号' or value == u'输入密码':
            eval(en).delete(0, END)
        if en == 'self.en_passwd':
            eval(en).config(show='*')

    # 显示数据
    def send_info(self):
        """打印信息，写入新信息"""
        en1_value = self.en_user.get().strip()
        en2_value = self.en_passwd.get().strip()
        date_value = self.date_chosen.get()  # get()方法是必需的
        startTime_value = self.startTime.get()
        endTime_value = self.endTime.get()

        txt = u'''
        学号:  %s 
        密码:  %s 
        ''' % (self.en_user.get(), self.en_passwd.get())
        if en1_value == '' or en1_value == u'输入学号':
            showwarning(u'无学号', u'请输入学号')
        elif en2_value == '' or en2_value == u'输入密码':
            showwarning(u'无密码', u'请输入密码')
        else:
            # 接收到学号和密码的情况
            # showinfo('学号密码', txt)
            # 打开文件取出数据并修改，然后存入变量
            with open(config_path, 'r') as f:
                config_before = json.load(f)
                config_before["username"] = en1_value
                config_before["password"] = en2_value
                config_before["date_flag"] = date_value
                config_before["startTime"] = startTime_value
                config_before["endTime"] = endTime_value

                config_after = config_before

            # 打开文件并覆盖写入修改后内容
            with open(config_path, 'w') as f:
                json.dump(config_after, f)
                # print config_after
                showinfo("参数列表", "username: " + config_after["username"] + "\n" +"date: " + config_after["date_flag"] +
                         "\n" + "start time: " + config_after["startTime"] + "\n" + "end time: " + config_after["endTime"])

            # 关掉对话框
            self.root.destroy()

    def enter_print(self, event):
        """提交"""
        self.send_info()


if __name__ == "__main__":
    Login()
