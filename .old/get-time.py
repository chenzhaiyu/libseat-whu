import time, datetime

def get_time(flag="tomorrow"):
    localtime = datetime.datetime.now()
    if flag == "tomorrow":
        delta = datetime.timedelta(days=1)
        date = localtime + delta

    return date.strftime('%Y-%m-%d')

if __name__ == '__main__':
    get_time()