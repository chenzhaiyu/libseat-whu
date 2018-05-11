# coding:utf-8

import httplib
import urllib
import random
import json
import time
import datetime
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# @ whu图书馆座位预约程序
# @ author:  czy
# @ email:   contact@chenzhaiyu.com
# @ website: http://www.chenzhaiyu.com


def load_config(config_path="config.json"):
    """导入config.json中的参数"""
    with open(config_path, 'r') as f:
        config = json.loads(f.read())
        # print config
        return config


def get_date(flag="tomorrow"):
    """获取当前日期，预定次日或今日座位"""
    localtime = datetime.datetime.now()
    if flag == "tomorrow":
        delta = datetime.timedelta(days=1)
        date = localtime + delta
    if flag == "today":
        date = localtime

    return date.strftime('%Y-%m-%d')


def get_token(config):
    """获取token值来授权登录, 使用HTTP GET方法"""
    login_url = "https://seat.lib.whu.edu.cn/rest/auth?username=" + str(config["username"]) + "&" + "password=" + str(
        config["password"])
    connection = httplib.HTTPConnection("seat.lib.whu.edu.cn")

    # 构造GET阶段的HTTP headers，伪装浏览器访问，防止被403，不过App端好像只使用了keep-alive参数
    headers_to_send = {
        # 'Connection': 'keep-alive',
        # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
        #               'Safari/537.11',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        # 'Accept-Encoding': 'none',
        # 'Accept-Language': 'en-US,en;q=0.8',
        }

    # 使用HTTP GET方法
    request = connection.request(method="GET", url=login_url, headers=headers_to_send)
    response = connection.getresponse()
    headers_received = response.getheaders()
    response = response.read()

    print "Headers info(get-token): \n" + str(headers_received) + "\n"
    print "Response info(get-token): \n" + response + "\n"
    # json.load() -> type: dict

    if json.loads(response)["data"]:
        token = json.loads(response)["data"]["token"]
        return token, response
    else:
        token = None
        return token, response
    # print token


def get_user_info(token):
    info_url = "https://seat.lib.whu.edu.cn:8443/rest/v2/user"
    connection = httplib.HTTPConnection("seat.lib.whu.edu.cn")
    headers_to_send = {'Host': 'seat.lib.whu.edu.cn:8443', 'Accept-Language': 'zh-cn',
                       'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Connection': 'keep-alive',
                       'token': str(token), 'User-Agent': 'doSingle/11 CFNetwork/893.14.2 Darwin/17.3.0'}
    request = connection.request(method="GET", url=info_url, headers=headers_to_send)
    response = connection.getresponse().read()
    #print "Response info(get-info): \n" + response + "\n"
    info_json = json.loads(response)["data"]
    userinfo = json.dumps(info_json).decode('unicode-escape')
    if userinfo:
        return userinfo
    else:
        pass


def post_data(seats ,config, token, index):
    """预定座位，通过选定座位号/时间/日期等，使用HTTP POST方法"""
    reserve_url = "https://seat.lib.whu.edu.cn:8443/rest/v2/freeBook"

    # POST到服务器的参数如下
    token_pure = token
    startTime = config["startTime"]
    endTime = config["endTime"]
    date = get_date(config["date_flag"])
    test = seats.values()
    seat = seats.values()[index]

    # token_data由纯token值添加起止时间和日期参数构成
    token_data = {"startTime": str(startTime), "endTime": str(endTime), "seat": int(seat), "date": str(date), "t": "1", "t2": "2"}
    token = urllib.urlencode(token_data)

    connection = httplib.HTTPConnection("seat.lib.whu.edu.cn")

    # 构造POST阶段的HTTP headers
    headers_to_send = {'Host': 'seat.lib.whu.edu.cn:8443', 'Accept-Language': 'zh-cn', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Connection': 'keep-alive', 'token': str(token_pure), 'User-Agent': 'doSingle/11 CFNetwork/893.14.2 Darwin/17.3.0'}
    """
    # 似乎不对的POST方式
    # 使用HTTP POST方法
    # request = connection.request(method="POST", url=url, body=str(token), headers=headers_to_send)
    # response = connection.getresponse()
    # headers_received = response.getheaders()
    # response = response.read()
    

    print "Headers info(post-data): \n" + str(headers_received) + "\n"
    print "Response info(post-data): \n" + str(response)
    status = json.loads(response)["status"]
    return status, response
    """

    # 新的POST方式
    response = requests.post(url=reserve_url, headers=headers_to_send, data=token_data, verify=False)
    response_json = response.json()
    msg = json.dumps(response_json).decode('unicode-escape')
    print msg
    if response_json[u"message"] == u'\u5df2\u67091\u4e2a\u6709\u6548\u9884\u7ea6\uff0c\u8bf7\u5728\u4f7f\u7528\u7ed3\u675f\u540e\u518d\u6b21\u8fdb\u884c\u9009\u62e9':
        return "已有预约", "已有预约"
    if response_json[u"message"] == u'\u7cfb\u7edf\u53ef\u9884\u7ea6\u65f6\u95f4\u4e3a 01:00 ~ 21:30':
        return "时间非法", "时间非法"
    if response_json[u'message'] == u'\u53c2\u6570\u9519\u8bef':
        return "参数错误", "参数错误"
    return response_json["status"], str(msg)


# 搜索指定时间和房间内的座位
# TODO: 全都是可用座位吗？
def search_seats(token, room, date):
    """根据房间号和时间返回座位号"""
    search_url = "https://seat.lib.whu.edu.cn:8443/rest/v2/room/layoutByDate/" + room + "/" + date

    headers_to_send = {'Host': 'seat.lib.whu.edu.cn:8443', 'Accept-Language': 'zh-cn',
                       'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Connection': 'keep-alive',
                       'token': str(token), 'User-Agent': 'doSingle/11 CFNetwork/893.14.2 Darwin/17.3.0'}
    response = requests.get(search_url, headers=headers_to_send, verify=False)
    json = response.json()
    print(json['status'])
    if json['status'] == 'success':
        allSeats = {}
        for seat in json['data']['layout']:
            if json['data']['layout'][seat]['type'] == 'seat':
                allSeats[json['data']['layout'][seat]['name']] = str(json['data']['layout'][seat]['id'])
        return allSeats
    else:
        print(json)
        return False


def schedule_run(config):
    """定时执行，通过监控当前时间与设定的触发时间比较，实现得很笨拙，在Linux/macOS下能设置定时任务的略过"""
    schedule_flag = config["schedule_flag"]
    schedule_time = config["schedule_time"]
    # 非定时执行模式
    if schedule_flag == "0":
        pass

    # 定时执行模式
    while schedule_flag == "1":
        time.sleep(random.uniform(0.8, 2.0))
        print "------------suspending------------"
        # 检查当前时刻
        hour_now = datetime.datetime.now().hour
        minute_now = datetime.datetime.now().minute
        second_now = datetime.datetime.now().second
        if hour_now > int(schedule_time[0]):
            break
        if hour_now >= int(schedule_time[0]) and minute_now >= int(schedule_time[1]):
            break
        if hour_now >= int(schedule_time[0]) and minute_now >= int(schedule_time[1]) and second_now >= int(schedule_time[2]):
            break
        # 当在设定时间前1小时前区间，休眠1h/次
        elif hour_now < int(schedule_time[0]) - 1:
            time.sleep(3600)
        # 当在设定时间前1小时至前15分钟区间，休眠10min/次
        elif hour_now == int(schedule_time[0]) - 1:
            time.sleep(600)
        # 当在设定时间前15分钟内区间，休眠1min/次
        elif hour_now == int(schedule_time[0]) and minute_now < int(schedule_time[1]) - 1:
            time.sleep(60)


def _format_address(s):
    """格式化邮件地址"""
    name, address = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        address.encode('utf-8') if isinstance(address, unicode) else address))


def send_mail(config, response):
    """用SMTP方式发送日志邮件，告知选座情况"""
    if config["send_mail_flag"] == "0":
        pass

    elif config["send_mail_flag"] == "1":
        address_from = config["mail_address_from"]
        password = config["mail_password"]
        address_to = config["mail_address_to"]
        smtp_server = config["mail_smtp_server"]

        text = "local time: {time_val}\nlogs: {log_val}".format(time_val=str(time.asctime()), log_val=response)
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = _format_address(u'localhost <%s>' % address_from)
        msg['To'] = _format_address(u'anybody <%s>' % address_to)
        msg['Subject'] = Header(u'每日图书饭日志', 'utf-8').encode()

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(address_from, password)
        server.sendmail(address_from, [address_to], msg.as_string())
        server.quit()


if __name__ == '__main__':
    """主函数"""
    global response
    config = load_config()
    schedule_run(config)
    token = get_token(config)
    index = 0

    while index < len(config["seats"]):
        status, response = post_data(config, token, index)
        index = index + 1
        time.sleep(random.uniform(0.1, 0.4))
        if status == "success":
            print "\n-------------Yeah! it's done!-------------\n"
            break
        else:
            print "\n--------------Oops! failed!---------------\n"
    send_mail(config, response)
