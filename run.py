# coding:utf-8

import functions
import time
import random


def run(config):
    """主函数，调用 function.py 的函数"""
    # TODO: 减少对 config.json 的调用次数，导入一次就够了
    functions.schedule_run(config)
    token, login_response = functions.get_token(config)

    if token:
        userinfo = functions.get_user_info(token)
        index = 0
        date = functions.get_date("today")
        seats = functions.search_seats(token, config["room"], date)

        while seats is not False and index < len(seats):
            status, response = functions.post_data(seats, config, token, index)
            index = index + 1
            time.sleep(random.uniform(0.1, 0.5))
            if status == "时间非法" or status == "已有预约" :#or status == "参数错误":
                print "\n------------" + status + "-------------"
                break
            if status == "success":
                print "\n-------------Yeah! it's done!-------------\n"
                break
            # TODO: 将所有除了success和该座位已被预约以外的status设置为返回status并break
            else:
                print "\n--------------Oops! failed!---------------\n"
        # TODO: 调整send_mail参数
        functions.send_mail(config, response)

    else:
        status = "fail"
        response = login_response

    return userinfo, status, response


if __name__ == '__main__':
    """直接运行 run.py 的情况，会使用 config.json 中缺省的参数来执行"""
    config = functions.load_config()
    run(config)
