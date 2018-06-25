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
            response = functions.post_data(seats, config, token, index)
            status = response[u"status"]
            index = index + 1
            time.sleep(random.uniform(0.1, 0.5))

            if status == u"fail":
                print "\n--------------Oops! failed!---------------\n"
                print "\n------------" + response[u'message'] + "-------------"
                break

            elif status == u"success":
                print "\n-------------Yeah! it's done!-------------\n"
                break

            # TODO: 将所有除了success和该座位已被预约以外的status设置为返回status并break

        # TODO: 调整send_mail参数
        functions.send_mail(config, response[u'message'])

    else:
        response = None

    return userinfo, response


if __name__ == '__main__':
    """直接运行 run.py 的情况，会使用 config.json 中缺省的参数来执行"""
    config = functions.load_config()
    run(config)
