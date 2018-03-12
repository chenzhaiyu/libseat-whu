# !/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
from tkFont import Font
from tkMessageBox import *
import json
import ttk
from functions import load_config
import run


config_path = "_config.json"


class GUI(object):
    """GUI对象"""
    def __init__(self):
        self.root = Tk()
        self.root.title(u'武汉大学图书馆座位自动预约系统(Beta)')
        self.root.resizable(True, True)
        self.root.geometry('+450+250')
        # self.root.geometry('350x150')
        self.sysfont = Font(self.root, size=14)

        RELIEF = ["flat", "raised", "sunken", "solid", "ridge", "groove"]

        # 学号，密码label
        self.lb_user = Label(self.root, text=u'学号:', padx=8, pady=10)
        self.lb_passwd = Label(self.root, text=u'密码:', padx=8)
        self.lb_user.grid(row=0, column=0, sticky=W)
        self.lb_passwd.grid(row=1, column=0, sticky=W)

        # 学号，密码entry
        self.en_user = ttk.Entry(self.root, font=self.sysfont, width=22)
        self.en_passwd = ttk.Entry(self.root, font=self.sysfont, width=22)
        self.en_user.grid(row=0, column=1, columnspan=2, padx=2)
        self.en_passwd.grid(row=1, column=1, columnspan=2, padx=2)

        # 从config.json中读取用户名和密码
        self.en_user.insert(0, self.load_config_before()["username"])
        self.en_passwd.insert(0, self.load_config_before()["password"])  # 隐藏密码
        self.en_passwd.config(show='*')

        self.en_user.config(validate='focusin',
                            validatecommand=lambda: self.validate_func('self.en_user'),
                            invalidcommand=lambda: self.invalid_func('self.en_user'))
        self.en_passwd.config(validate='focusin',
                              validatecommand=lambda: self.validate_func('self.en_passwd'),
                              invalidcommand=lambda: self.invalid_func('self.en_passwd'))
        # 记住密码checkbutton
        self.ckb_remember_var = IntVar()
        self.ckb_remember = Checkbutton(self.root, text=u'记住密码', underline=0, variable=self.ckb_remember_var)
        self.ckb_remember.select()
        self.ckb_remember.grid(row=3, column=0)

        # 启用邮件通知checkbutton
        self.ckb_email_var = IntVar()
        self.ckb_email = Checkbutton(self.root, text=u'启用邮件通知', underline=0, variable=self.ckb_email_var)
        self.ckb_email.select()
        self.ckb_email.grid(row=3, column=1)

        # # 邮件参数设置表单label
        # self.lb_email_sender = Label(self.root, text=u'发件邮箱:', padx=8)
        # self.lb_email_smtp = Label(self.root, text=u'邮箱密码:', padx=8)
        # self.lb_email_passwd = Label(self.root, text=u'smtp服务器:', padx=8)
        # self.lb_email_receiver = Label(self.root, text=u'收件邮箱:', padx=8)
        # self.lb_email_sender.grid(row=5, column=0, sticky=W)
        # self.lb_email_passwd.grid(row=6, column=0, sticky=W)
        # self.lb_email_smtp.grid(row=7, column=0, sticky=W)
        # self.lb_email_receiver.grid(row=8, column=0, sticky=W)
        #
        # # 邮件参数设置表单entry
        # self.en_email_sender = ttk.Entry(self.root, font=self.sysfont, width=22)
        # self.en_email_passwd = ttk.Entry(self.root, font=self.sysfont, width=22)
        # self.en_email_smtp = ttk.Entry(self.root, font=self.sysfont, width=22)
        # self.en_email_receiver = ttk.Entry(self.root, font=self.sysfont, width=22)
        # self.en_email_sender.grid(row=5, column=1, columnspan=2, padx=2, pady=2)
        # self.en_email_passwd.grid(row=6, column=1, columnspan=2, padx=2, pady=2)
        # self.en_email_smtp.grid(row=7, column=1, columnspan=2, padx=2, pady=2)
        # self.en_email_receiver.grid(row=8, column=1, columnspan=2, padx=2, pady=2)

        # 确定按钮
        self.bt_print = ttk.Button(self.root, text=u'确定')
        self.bt_print.grid(row=3, column=2, pady=3)
        self.bt_print.config(command=self.process_func)
        self.root.bind('<Return>', self.enter_print)

        # 日期下拉列表
        self.date = StringVar()
        self.date_chosen = ttk.Combobox(self.root, width=5, textvariable=self.date, state='readonly')
        self.date_chosen['values'] = ("today", "tomorrow")  # 设置下拉列表的值
        self.date_chosen.grid(column=0, row=2, pady=8, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.date_chosen.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 起始时间下拉列表
        self.startTime = StringVar()
        self.startTime_chosen = ttk.Combobox(self.root, width=7, textvariable=self.startTime, state='readonly')
        self.startTime_chosen['values'] = ("08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00")  # 设置下拉列表的值
        self.startTime_chosen.grid(column=1, row=2, padx=10)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.startTime_chosen.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 终止时间下拉列表
        self.endTime = StringVar()
        self.endTime_chosen = ttk.Combobox(self.root, width=7, textvariable=self.endTime, state='readonly')
        self.endTime_chosen['values'] = ("08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00")  # 设置下拉列表的值
        self.endTime_chosen.grid(column=2, row=2)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.endTime_chosen.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 信息栏Text
        self.info = Text(self.root, height=8, width=30, state="normal")
        self.info.grid(column=4, row=0, rowspan=4, padx=5)
        self.info.insert(END, "Runtime Info:\n\n")
        self.info.insert(END, "[22:15-23:50可预约明日座位]\n\n")
        self.info.insert(END, "[场馆/楼层/房间暂未适配好，执行选座会默认选座到信息分馆云桌面]\n\n")
        self.info.focus()

        # 分馆下拉列表
        self.lib = StringVar()
        self.cbb_lib = ttk.Combobox(self.root, width=10, textvariable=self.lib, state='disabled')
        self.cbb_lib['values'] = ("信息分馆", "工学分馆", "医学分馆", "总馆")  # 设置下拉列表的值
        self.cbb_lib.bind('<<ComboboxSelected>>', self.cbb_lib_selected)  # 绑定虚拟事件：cbb选值
        self.cbb_lib.grid(column=3, row=0, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.cbb_lib.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 楼层下拉列表
        self.floor = StringVar()
        self.cbb_floor = ttk.Combobox(self.root, width=10, textvariable=self.floor, state='readonly')
        self.cbb_floor['values'] = ("一楼", "二楼", "三楼", "四楼")  # 设置下拉列表的值
        self.cbb_floor.bind('<<ComboboxSelected>>', self.cbb_floor_selected)  # 绑定虚拟事件：cbb选值
        self.cbb_floor.grid(column=3, row=1, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.cbb_floor.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 房间下拉列表
        self.room = StringVar()
        self.cbb_room = ttk.Combobox(self.root, width=10, textvariable=self.room, state='readonly')
        # TODO: 用户可能使用缺省的分馆和楼层（没有cbb_floor_selected虚拟事件），缺省的房间必须对应缺省分馆和缺省楼层
        self.cbb_room['values'] = ("双屏电脑", "电子资源阅览区", "3C创客空间", "创新学习讨论区", "MAC电脑", "云桌面")  # 设置下拉列表的值
        self.cbb_room.bind('<<ComboboxSelected>>', self.cbb_room_selected)  # 绑定虚拟事件：cbb选值
        self.cbb_room.grid(column=3, row=2, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.cbb_room.current(5)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 座位下拉列表
        self.seat = StringVar()
        self.cbb_seat = ttk.Combobox(self.root, width=10, textvariable=self.seat, state='readonly')
        # TODO: 用户可能使用缺省的分馆和楼层和房间（没有cbb_floor_selected虚拟事件），缺省的房间必须对应缺省分馆，缺省楼层和缺省房间
        self.cbb_seat['values'] = ["%03d" % i for i in range(1, 21)]  # 设置下拉列表的值
        self.cbb_seat.grid(column=3, row=3, padx=3)  # 设置其在界面中出现的位置, column代表列, row 代表行
        self.cbb_seat.current(0)  # 设置下拉列表默认显示的值, 0为numberChosen['values']的下标值

        # 关于栏Text
        # TODO: 关于栏显示程序信息
        # self.info = Text(self.root, height=8, width=30, state="normal")
        # self.info.grid(column=0, row=4, columnspan=4, padx=5)
        # self.info.insert(END, "runtime info:\n")
        # self.info.insert(END, "22:15-23:50可预约明日座位\n")
        # self.info.focus()

        # 显示小图片
        logo = PhotoImage(file='src/logo.gif')
        lb_logo = Label(self.root, image=logo, height=130)
        lb_logo.grid(row=0, column=5, rowspan=4, padx=1)


        self.root.mainloop()

    def cbb_lib_selected(self, event):
        """选定cbb_lib时触发函数"""
        # TODO: 除信息分馆歪，其他馆还没适配
        if self.lib.get() == u"信息分馆":
            self.cbb_floor['values'] = ["一楼", "二楼", "三楼", "四楼"]
        elif self.lib.get() == u"总馆":
            self.cbb_floor['values'] = ["一楼", "二楼", "三楼", "四楼", "五楼"]
        elif self.lib.get() == u"工学分馆":
            self.cbb_floor['values'] = ["一楼", "二楼", "三楼", "四楼", "五楼"]
        elif self.lib.get() == u"医学分馆":
            self.cbb_floor['values'] = ["一楼", "二楼", "三楼", "四楼", "五楼"]

    def cbb_floor_selected(self, event):
        """选定cbb_floor时触发函数"""
        if self.floor.get() == u"一楼":
            self.cbb_room['values'] = ["双屏电脑", "电子资源阅览区", "3C创客空间", "创新学习讨论区", "MAC电脑", "云桌面"]
        if self.floor.get() == u"二楼":
            self.cbb_room['values'] = ["二楼东", "二楼西"]
        if self.floor.get() == u"三楼":
            self.cbb_room['values'] = ["三楼东", "三楼自主学习区", "三楼西"]
        if self.floor.get() == u"四楼":
            self.cbb_room['values'] = ["四楼东", "四楼西"]

    def cbb_room_selected(self, event):
        """选定cbb_floor时触发函数"""
        if self.room.get() == u"双屏电脑":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 21)]
        if self.room.get() == u"电子资源阅览区":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 21)]
        if self.room.get() == u"3C创客空间":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 111)]
        if self.room.get() == u"创新学习讨论区":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 65)]
        if self.room.get() == u"MAC电脑":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 13)]
        if self.room.get() == u"云桌面":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 43)]
        if self.room.get() == u"二楼东":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 93)]
        if self.room.get() == u"二楼西":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 93)]
        if self.room.get() == u"三楼东":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 85)]
        if self.room.get() == u"三楼自主学习区":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 189)]
        if self.room.get() == u"三楼西":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 89)]
        if self.room.get() == u"四楼东":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 81)]
        if self.room.get() == u"四楼西":
            self.cbb_seat['values'] = ["%03d" % i for i in range(1, 89)]

    def load_config_before(self):
        """从config.json中读取原来的配置"""
        return load_config(config_path)

    def validate_func(self, en):
        """验证输入"""
        return False if eval(en).get().strip() != '' else True

    def invalid_func(self, en):
        """没什么用"""
        value = eval(en).get().strip()
        if value == u'输入学号' or value == u'输入密码':
            eval(en).delete(0, END)
        if en == 'self.en_passwd':
            eval(en).config(show='*')

    def process_func(self):
        """GUI部分的主函数，允许用户在窗口修改 config.json 的参数，并调用 run.py 执行选座"""
        # TODO: 改混乱的变量名
        en1_value = self.en_user.get().strip()
        en2_value = self.en_passwd.get().strip()
        date_value = self.date_chosen.get()  # get()方法是必需的
        startTime_value = int(self.startTime.get().split(":")[0]) * 60 + int(self.startTime.get().split(":")[1])
        endTime_value = int(self.endTime.get().split(":")[0]) * 60 + int(self.endTime.get().split(":")[1])
        email_value = str(self.ckb_email_var.get())
        remember_value = str(self.ckb_remember_var.get())

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

                # 复选框选中则保存密码，否则清空
                if remember_value == "1":
                    config_before["password"] = en2_value
                else:
                    config_before["password"] = ''

                # 日期选择为today时禁用预约模式，为tomorrow时启用预约模式，而是否进入suspending则由 functions.py 中的schedule_run判断
                if date_value == "today":
                    config_before["schedule_flag"] = "0"
                elif date_value == "tomorrow":
                    config_before["schedule_flag"] = "1"

                # 保存在GUI中设置的日期，起止时间，是否启用邮件提醒
                config_before["date_flag"] = date_value
                config_before["startTime"] = str(startTime_value)
                config_before["endTime"] = str(endTime_value)
                config_before["send_mail_flag"] = email_value
                config_after = config_before

            # 打开文件并覆盖写入修改后内容
            with open(config_path, 'w') as f:
                json.dump(config_after, f)

            # TODO: 写入info框
            self.info.insert(END, "------用户设置已保存------\n")
            self.info.insert(END, "------开始运行主程序------\n")

            # 调用 run.py 执行选座流程
            status, response = run.run(config_after)
            self.info.insert(END, response)
            self.info.insert(END, "\n")

            # TODO: 以合适的方式结束对话框
            # TODO: showinfo
            # self.root.destroy()

    def enter_print(self):
        """提交"""
        self.process_func()


if __name__ == "__main__":
    GUI()
