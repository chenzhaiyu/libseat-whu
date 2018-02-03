# coding:utf-8

import httplib
import urllib, urllib2
url = "http://seat.lib.whu.edu.cn/rest/v2/freeBook"

# parameters below
token_pure = "BFFC8MKLI001294456"
startTime = "-1"
endTIme = "1530"
seat = "9396"
date = "2018-01-29"
# parameters above

token_data = {"token": token_pure, "startTime": startTime, "endTime": endTIme, "seat": seat, "date": date}
token = urllib.urlencode(token_data)
print "token-to-send: " + token

connection = httplib.HTTPConnection("seat.lib.whu.edu.cn")

# headers_sent = {"Connection": "Keep-alive", "Content-Length": "76",
# "Content-Type": "application/x-www-form-urlencoded", "token": token}

headers_to_send = {"Connection": "Keep-alive", "Content-Length": "76", "Content-Type": "application/x-www-form-urlencoded"}
data_to_send = token

request = connection.request(method="POST", url=url, body=str(data_to_send), headers=headers_to_send)
response = connection.getresponse()
headers_received = response.getheaders()
response = response.read()

print "Headers info: \n" + str(headers_received) + "\n"
print "Response info: \n" + str(response)