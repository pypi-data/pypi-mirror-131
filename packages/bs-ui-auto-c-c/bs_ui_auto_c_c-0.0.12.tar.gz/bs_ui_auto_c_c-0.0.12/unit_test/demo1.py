import time

import requests

from b_c_components.log.log import Logging

loger = Logging('log.txt')

str_data = ''
with open('1.txt', 'r') as f:
    str_data = f.read()
data_list = str_data.replace('\n', ',').split(',')
# data_list = [
#     64826298,
#     64826299
# ]
while data_list:
        snId = data_list.pop(0)
        data = {
            'tenantId': 101113,
            'activityId': '',
            'snId': snId
        }
        headers = {
            # 'content-type': ' application/x-www-form-urlencoded;charse=UTF-8'
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://apschoice.ceping.com/Home/Ops?user=assessment&pwd=aps',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'OpenccCookieName=zh-CN;assessuniversity=;assessIp=58.240.123.86',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"'

        }
        session = requests.session()
        r = session.post('https://apschoice.ceping.com/Home/ReCalScore', headers=headers, data=data)
        loger.logger.info(msg=str(snId) + r.text)
        print(str(snId) + r.text)
