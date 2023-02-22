#!usr/bin/python3

import random
from time import localtime
from requests import get, post
import datetime
from zhdate import ZhDate
import sys
import os
import json
import http.client
import urllib

myAPIKEY = '73a41c7551c965462ed783eb8dcaddb7'

g_cities = []
g_weathers = []


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: '#' + '%06x' % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_token():
    # appId
    app_id = users['app_id']
    # appSecret
    app_secret = users['app_secret']
    post_url = ('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'
                .format(app_id, app_secret))
    try:
        token = get(post_url).json()['access_token']
    except KeyError:
        print('获取token失败，请检查app_id和app_secret是否正确')
        os.system('pause')
        sys.exit(1)
    # print(token)
    return token


def get_weather_city_info(province, city):
    conn = http.client.HTTPSConnection('apis.tianapi.com')  # 接口域名
    params = urllib.parse.urlencode({'key': myAPIKEY, 'area': city})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn.request('POST', '/citylookup/index', params, headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode('utf-8')
    dict_data = json.loads(data)

    if dict_data['code'] != 200:
        return 'error'

    for item in dict_data['result']['list']:
        if item['provincecn'] == province:
            return item

    return 'error'


def get_weather(province, city):
    # find cache
    if g_cities.count(province + city):
        return g_weathers[province + city]

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

    if dict_data['code'] != 200:
        return 'error'

    # add this to cache
    g_cities.append(province + city)
    g_weathers.append({province + city, dict_data['result']})
    return dict_data['result']


def get_ciba():
    url = 'http://open.iciba.com/dsapi/'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    r = get(url, headers=headers)
    dict_data = r.json()
    if r.status_code == 200 and dict_data:
        return dict_data

    return 'error'


def get_holiday():
    url = 'https://wangxinleo.cn/api/wx-push/holiday/getHolidaytts'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)

    dict_data = r.json()
    if dict_data['code'] == 0 and r.status_code == 200 and dict_data:
        return dict_data

    return 'error'


def get_morning_greeting():
    conn = http.client.HTTPSConnection('apis.tianapi.com')  # 接口域名
    params = urllib.parse.urlencode({'key': myAPIKEY})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn.request('POST', '/zaoan/index', params, headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode('utf-8')
    dict_data = json.loads(data)

    if dict_data['code'] != 200:
        return 'error'

    return dict_data['result']


def get_evening_greeting():
    conn = http.client.HTTPSConnection('apis.tianapi.com')  # 接口域名
    params = urllib.parse.urlencode({'key': myAPIKEY})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn.request('POST', '/wanan/index', params, headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode('utf-8')
    dict_data = json.loads(data)

    if dict_data['code'] != 200:
        return 'error'

    return dict_data['result']


def get_love_poetry():
    conn = http.client.HTTPSConnection('apis.tianapi.com')  # 接口域名
    params = urllib.parse.urlencode({'key': myAPIKEY})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn.request('POST', '/qingshi/index', params, headers)
    tianapi = conn.getresponse()
    result = tianapi.read()
    data = result.decode('utf-8')
    dict_data = json.loads(data)

    if dict_data['code'] != 200:
        return 'error'

    return dict_data['result']


def get_template_data(user):
    # get weather
    weather = get_weather(user['province'], user['city'])
    if weather == 'error':
        print('get weather infomation error!')
        return weather
    # get holiday
    holiday = get_holiday()
    if holiday == 'error':
        print('get holiday infomation error!')
        return holiday
    # get greeting
    morning_greeting = get_morning_greeting()
    evening_greeting = get_evening_greeting()
    if morning_greeting == 'error':
        print('get morning greeting error!')
        return morning_greeting
    if evening_greeting == 'error':
        print('get evening greeting error!')
        return evening_greeting
    # get ciba
    ciba = get_ciba()
    if ciba == 'error':
        print('get ciba infomation error!')
        return ciba
    # get love poetry
    love_poetry = get_love_poetry()
    if love_poetry == 'error':
        print('get love poetry error!')
        return love_poetry

    # current date
    c_time = weather['date'].split('-')
    c_date = datetime.datetime(int(c_time[0]), int(c_time[1]), int(c_time[2]))

    data = {
        'date': {
            'value': '{}年{}月{}日 {}'.format(c_time[0], c_time[1], c_time[2], weather['week']),
            'color': get_color()
        },
        'province': {
            'value': weather['province'],
            'color': get_color()
        },
        'city': {
            'value': weather['area'],
            'color': get_color()
        },
        'weather': {
            'value': weather['weather'],
            'color': get_color()
        },
        'min_temperature': {
            'value': weather['lowest'],
            'color': get_color()
        },
        'max_temperature': {
            'value': weather['highest'],
            'color': get_color()
        },
        'wind_direction': {
            'value': weather['wind'],
            'color': get_color()
        },
        'wind_scale': {
            'value': weather['windsc'],
            'color': get_color()
        },
        'humidity': {
            'value': weather['humidity'],
            'color': get_color()
        },
        'sunrise': {
            'value': weather['sunrise'],
            'color': get_color()
        },
        'sundown': {
            'value': weather['sunset'],
            'color': get_color()
        },
        'moonrise': {
            'value': weather['moonrise'],
            'color': get_color()
        },
        'moondown': {
            'value': weather['moondown'],
            'color': get_color()
        },
        'air_quality': {
            'value': weather['quality'],
            'color': get_color()
        },
        'weather_tips': {
            'value': weather['tips'],
            'color': get_color()
        },
        'holidaytts': {
            'value': holiday['tts'],
            'color': get_color()
        },
        'note_en': {
            'value': ciba['content'],
            'color': get_color()
        },
        'note_ch': {
            'value': ciba['note'],
            'color': get_color()
        },
        'morning_greeting': {
            'value': morning_greeting['content'],
            'color': get_color()
        },
        'evening_greeting': {
            'value': evening_greeting['content'],
            'color': get_color()
        },
        'love_poetry': {
            'value': love_poetry['content'],
            'color': get_color()
        }
        # '':{
        #     'value': ,
        #     'color': get_color()
        # },
        # '':{
        #     'value': ,
        #     'color': get_color()
        # },
        # '':{
        #     'value': ,
        #     'color': get_color()
        # },
        # '':{
        #     'value': ,
        #     'color': get_color()
        # },
        # '':{
        #     'value': ,
        #     'color': get_color()
        # },
    }

    # calculate memorial days
    for item in user['memorialdays']:
        i_key = item['key']
        i_time = item['date'].split('-')
        i_date = datetime.datetime(int(i_time[0]), int(i_time[1]), int(i_time[2]))

        i_days = (c_date - i_date).days
        data[i_key] = {
            'value': i_days,
            'color': get_color()
        }

    # calculate festivals
    for item in user['festivals']:
        i_key = item['key']
        i_time = item['date'].split('-')
        i_days = 0
        if i_key[0] == '*':
            luner_c_date = ZhDate.today()
            luner_t_date = ZhDate(int(i_time[0]), int(c_time[1]), int(c_time[2]))
            i_days = (luner_t_date.to_datetime() - luner_c_date.to_datetime()).days
            if i_days < 0:
                luner_t_date = ZhDate(int(i_time[0]) + 1, int(c_time[1]), int(c_time[2]))
                i_days = (luner_t_date.to_datetime() - luner_c_date.to_datetime()).days
        else:
            t_date = datetime.datetime(int(i_time[0]), int(c_time[1]), int(c_time[2]))
            i_days = (t_date - c_date).days
            if i_days < 0:
                t_date = datetime.datetime(int(i_time[0]) + 1, int(c_time[1]), int(c_time[2]))
                i_days = (t_date - c_date).days

        data[i_key] = {
            'value': i_days,
            'color': get_color()
        }

    print(data)
    return data


def get_data(user):
    data = {
        'touser': user['id'],
        'template_id': user['template_id'],
        'url': 'http://weixin.qq.com/download',
        'topcolor': '#FF0000',
        'data': get_template_data(user)
    }

    return data


def send(user, token):
    data = get_data(user)
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    r = post(url, headers=headers, json=data).json()
    if r['errcode'] == 40037:
        print('推送消息失败，请检查模板id是否正确')
    elif r['errcode'] == 40036:
        print('推送消息失败，请检查模板id是否为空')
    elif r['errcode'] == 40003:
        print('推送消息失败! id填写不正确！应该填用户扫码后生成的id！要么就是填错了！请检查配置文件！')
    elif r['errcode'] == 0:
        print('推送消息成功')
    else:
        print(r)


if __name__ == "__main__":
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        print('file not found!')
        os.system('pause')
        sys.exit(1)
    except SyntaxError:
        print('file format error!')
        os.system('pause')
        sys.exit(1)

    token = get_token()

    for user in users['users']:
        send(user, token)
