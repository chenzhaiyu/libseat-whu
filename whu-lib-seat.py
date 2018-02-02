# coding:utf-8

import httplib
import urllib
import random
import json
import time
import datetime

# @ whu图书馆座位预约程序
# @ author:  czy
# @ email:   contact@chenzhaiyu.com
# @ website: http://www.chenzhaiyu.com


def load_conf():
    """load from conf.json"""
    with open("conf-me.json", 'r') as f:
        conf = json.loads(f.read())
        # print conf
        return conf


def get_date(flag="tomorrow"):
    """add 1 day to the localtime, by default"""
    localtime = datetime.datetime.now()
    if flag == "tomorrow":
        delta = datetime.timedelta(days=1)
        date = localtime + delta
    if flag == "today":
        date = localtime

    return date.strftime('%Y-%m-%d')


def get_token():
    """get token to authorize login, using method GET"""
    # url = "http://seat.lib.whu.edu.cn/rest/auth?username=2015xxxxxxxxx&password=15xxxx"
    url = "http://seat.lib.whu.edu.cn/rest/auth?username=" + str(conf["username"]) + "&" + "password=" + str(
        conf["password"])
    connection = httplib.HTTPConnection("seat.lib.whu.edu.cn")

    headers_to_send = {
        'Connection': 'keep-alive',
        # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        # 'Accept-Encoding': 'none',
        # 'Accept-Language': 'en-US,en;q=0.8',
        }

    request = connection.request(method="GET", url=url, headers=headers_to_send)
    response = connection.getresponse()
    headers_received = response.getheaders()
    response = response.read()

    print "Headers info(get-token): \n" + str(headers_received) + "\n"
    print "Response info(get-token): \n" + response + "\n"
    # json.load() -> type: dict
    token = json.loads(response)["data"]["token"]
    return token
    # print token


def post_data(token, conf, index):
    """pick up a seat, by seat number, time, date, using method POST"""
    url = "http://seat.lib.whu.edu.cn/rest/v2/freeBook"

    # parameters below
    token_pure = token
    startTime = conf["startTime"]
    endTIme = conf["endTime"]
    date = get_date(conf["date_flag"])
    seats = conf["seats"]
    seat = seats[index]
    # parameters above

    token_data = {"token": token_pure, "startTime": startTime, "endTime": endTIme, "seat": seat, "date": date}
    token = urllib.urlencode(token_data)
    # print "token-to-send: " + token + "\n"

    connection = httplib.HTTPConnection("seat.lib.whu.edu.cn")

    headers_to_send = {"Connection": "Keep-alive", "Content-Length": "76",
                       "Content-Type": "application/x-www-form-urlencoded"}

    request = connection.request(method="POST", url=url, body=str(token), headers=headers_to_send)
    response = connection.getresponse()
    headers_received = response.getheaders()
    response = response.read()

    print "Headers info(post-data): \n" + str(headers_received) + "\n"
    print "Response info(post-data): \n" + str(response)
    status = json.loads(response)["status"]
    return status


def schedule_run(conf):
    """schedule run, according to time set in conf.json"""
    schedule_flag = conf["schedule_flag"]
    schedule_time = conf["schedule_time"]
    if schedule_flag == "0":
        pass

    while schedule_flag == "1":
        print "------------suspending------------"
        # 检查当前时刻
        hour_now = datetime.datetime.now().hour
        minute_now = datetime.datetime.now().minute
        second_now = datetime.datetime.now().second
        if hour_now >= int(schedule_time[0]) and minute_now >= int(schedule_time[1]) and second_now >= int(schedule_time[2]):
            break
        # 当在设定时间前1小时前区间，休眠1h/次
        elif hour_now < int(schedule_time[0]) - 1:
            time.sleep(3600)
            if minute_now < int(schedule_time[1] - 1):
                time.sleep(60)


if __name__ == '__main__':

    conf = load_conf()
    schedule_run(conf)
    token = get_token()
    index = 0
    while index < len(conf["seats"]):
        status = post_data(token, conf, index)
        index = index + 1
        time.sleep(random.uniform(0.1, 0.4))
        if status == "success":
            print "\n-------------Yeah! it's done!-------------\n"
            break
        else:
            print "\n--------------Oops! failed!---------------"
            print "\n"