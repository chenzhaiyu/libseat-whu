# coding:utf-8

import functions
import time
import random


def run():
    """主函数，调用 function.py 的函数"""
    config = functions.load_config()
    functions.schedule_run(config)
    token = functions.get_token(config)
    index = 0

    while index < len(config["seats"]):
        status, response = functions.post_data(config, token, index)
        index = index + 1
        time.sleep(random.uniform(0.1, 0.4))
        if status == "success":
            print "\n-------------Yeah! it's done!-------------\n"
            break
        else:
            print "\n--------------Oops! failed!---------------\n"
    # TODO: 调整send_mail参数
    functions.send_mail(config, response)


if __name__ == '__main__':
    """直接运行 run.py 的情况，会使用 config.json 中缺省的参数来执行"""
    run()
