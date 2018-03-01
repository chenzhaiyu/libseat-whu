# !/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
from tkFont import Font
from tkMessageBox import *
import json
from functions import load_config


try:
    from ttk import Entry, Button
except ImportError:
    pass

config_path = "config.json"


class Login(object):

    def __init__(self):
        self.root = Tk()
        self.root.title(u'登录')
        self.root.resizable(False, False)
        self.root.geometry('+450+250')

        self.sysfont = Font(self.root, size=14)

        self.lb_user = Label(self.root, text=u'学号：', padx=5)
        self.lb_passwd = Label(self.root, text=u'密码：', padx=5)
        self.lb_user.grid(row=0, column=0, sticky=W)
        self.lb_passwd.grid(row=1, column=0, sticky=W)

        self.en_user = Entry(self.root, font=self.sysfont, width=18)
        self.en_passwd = Entry(self.root, font=self.sysfont, width=18)
        self.en_user.grid(row=0, column=1, columnspan=2)
        self.en_passwd.grid(row=1, column=1, columnspan=2)

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

        self.var = IntVar()
        self.ckb = Checkbutton(self.root, text=u'记住学号和密码', underline=0,
                               variable=self.var)
        self.ckb.grid(row=2, column=1)
        self.bt_print = Button(self.root, text=u'确定')
        self.bt_print.grid(row=2, column=2, sticky=E, pady=5)
        self.bt_print.config(command=self.send_info)

        self.root.bind('<Return>', self.enter_print)

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
