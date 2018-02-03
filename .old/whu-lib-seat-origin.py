# coding:utf-8

import httplib
import urllib, urllib2
import time
import json

def get_token():
    url = "http://seat.lib.whu.edu.cn/rest/auth?username=2015xxxxxxxxx&password=xxxxxx"

    connection = httplib.HTTPConnection("seat.lib.whu.edu.cn")
    headers_sent = {"Connection": "Keep-alive"}
    request = connection.request(method="GET", url=url, headers=headers_sent)
    response = connection.getresponse()
    headers_received = response.getheaders()
    response = response.read()

    print "Headers info(get-token): \n" + str(headers_received) + "\n"
    print "Response info(get-token): \n" + response + "\n"
    # json.load()以后转为dict类型
    token = json.loads(response)["data"]["token"]
    return token
    # print token


def post_data(token):
    url = "http://seat.lib.whu.edu.cn/rest/v2/freeBook"

    # parameters below
    token_pure = token
    startTime = "810"
    endTIme = "990"
    date = "2018-02-01"
    seats = ["9388", "9506", "9392", "9400", "9413", "9419", "9411", "9409", "9436", "9430", "9432", "9442", "9463",
             "9507", "9461", "9459", "9451", "9480", "9509", "9508", "9484", "9505", "9497", "9503", "9495", "9501", "9493"]
    seat = seats[0]
    # parameters above

    token_data = {"token": token_pure, "startTime": startTime, "endTime": endTIme, "seat": seat, "date": date}
    token = urllib.urlencode(token_data)
    # print "token-to-send: " + token + "\n"

    connection = httplib.HTTPConnection("seat.lib.whu.edu.cn")

    # headers_sent = {"Connection": "Keep-alive", "Content-Length": "76",
    # "Content-Type": "application/x-www-form-urlencoded", "token": token}

    headers_to_send = {"Connection": "Keep-alive", "Content-Length": "76",
                       "Content-Type": "application/x-www-form-urlencoded"}
    data_to_send = token
    request = connection.request(method="POST", url=url, body=str(data_to_send), headers=headers_to_send)
    response = connection.getresponse()
    headers_received = response.getheaders()
    response = response.read()

    print "Headers info(post-data): \n" + str(headers_received) + "\n"
    print "Response info(post-data): \n" + str(response)
    status = json.loads(response)["status"]
    return status


if __name__ == '__main__':
    token = get_token()
    time.sleep(0.1)
    seat_index = 0
    seat_index_max = 26
    while seat_index < seat_index_max:
        status = post_data(token)
        seat_index = seat_index + 1
        if status == "success":
            print "it's done"
            break