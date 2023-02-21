#!usr/bin/python3

import random
from time import localtime
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os
import json
import http.client
import urllib

myAPIKEY = '73a41c7551c965462ed783eb8dcaddb7'


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


# def get_access_token():
#     # appId
#     app_id = config["app_id"]
#     # appSecret
#     app_secret = config["app_secret"]
#     post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
#                 .format(app_id, app_secret))
#     try:
#         access_token = get(post_url).json()['access_token']
#     except KeyError:
#         print("获取access_token失败，请检查app_id和app_secret是否正确")
#         os.system("pause")
#         sys.exit(1)
#     # print(access_token)
#     return access_token


def get_weather_city_info(province, city):
    conn = http.client.HTTPSConnection('apis.tianapi.com')  # 接口域名
    params = urllib.parse.urlencode({'key': myAPIKEY, 'area': city})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn.request('POST', '/citylookup/index', params, headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode('utf-8')
    dict_data = json.loads(data)
    print(dict_data)
    if dict_data['code'] != 200:
        return 'error'

    for item in dict_data['result']['list']:
        if item['provincecn'] == province:
            return item

    return 'error'


def get_weather(province, city):
    city_info = get_weather_city_info(province, city)
    if city_info == 'error':
        return 'error'

    conn = http.client.HTTPSConnection('apis.tianapi.com')  # 接口域名
    params = urllib.parse.urlencode({'key': myAPIKEY, 'city': city_info['areaid'][2:], 'type': '1'})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn.request('POST', '/tianqi/index', params, headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode('utf-8')
    dict_data = json.loads(data)
    print(dict_data)

    if dict_data['code'] != 200:
        return 'error'

    return dict_data['result']


def get_holiday():
    pass


def get_data():
    pass


if __name__ == "__main__":
    # try:
    #     with open('config.json', 'r') as f:
    #         config = json.load(f)
    # except FileNotFoundError:
    #     print("file not found!")
    #     os.system("pause")
    #     sys.exit(1)
    # except SyntaxError:
    #     print("file format error!")
    #     os.system("pause")
    #     sys.exit(1)
    #
    # # get accessToken from file
    # accessToken = get_access_token()
    # # users
    #
    # data = get_data()

    # data = get_weather_city_info('山西', '西安')
    data = get_weather('山东', '莱州')
    print(data)

