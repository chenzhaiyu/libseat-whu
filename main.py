# coding:utf-8

import functions
import time
import random

if __name__ == '__main__':
    """主函数"""

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
    functions.send_mail(config, response)
