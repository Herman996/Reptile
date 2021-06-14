# encoding: utf-8
# author: herman_tang
import requests
import re
import json
import csv
import sys
import os

APIkey = 'eiaOYEz8eO9MpU3wKaz0WDA64xaGu2FU'
# city = input("请输入要查询的城市名: ")
city = "北京"
file1 = r'/data/shell/district_id.csv'

def is_chinese():
    count1 = len(city)
    count =0
    while count < count1:
        if '\u4e00' <= city[count] <= '\u9fff':
            number = 'True'
        else:
            number = 'False'
            break
        count += 1
    return number

def distr_id():
    with open(file1, 'r', encoding='utf-8') as filea:
        lines = csv.reader(filea)
        for i in lines:
            if i[5] == city:
                district_id = i[1]
    return district_id

def get_info(data_type: str ='all'):
    """
    这里传递的产生来data_type一共以下几种类型：
    1、all      所有信息
    2、now      实时数据
    3、alert    气象预警
    4、index    生活指数
    5、fc       预报数据
    6、fc_hour  未来24小时小时预报（高级字段）
    默认为all，返回所有的信息
    """
    try:
        district_id = distr_id()
    except:
        return "您输入的城市名{}不正确，请重新输入..........".format(city)
    url = "http://api.map.baidu.com/weather/v1/?district_id={}&data_type={}&output=json&ak={}".format(district_id, data_type, APIkey)
    payload = {}
    headers = {
    'Cookie': 'BAIDUID=F47B1A43BB52CB5876036267ABD4EEC7:FG=1',
    "Content-Type": "application/json"
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    info = json.dumps(json.loads(response.text), ensure_ascii=False)
    weather_info = eval(info)
    return weather_info

def P_info():
    '''
    这里是调用get_info函数，解析获取到的信息，将信息进行转换
    '''
    # print(get_info())
    weather_info = get_info()['result']
    now = weather_info['now']
    futrue = weather_info['forecasts']
    country = weather_info['location']['country']
    province = weather_info['location']['province']
    city = weather_info['location']['city']
    county = weather_info['location']['name']
    text = now['text']
    temp = now['temp']
    feels_like = now['feels_like']
    rh = now['rh']
    wind_class = now['wind_class']
    wind_dir = now['wind_dir']
    #now = '实时数据:'
    '''
    这里是获取当天天气信息
    '''
    if county == city[:-1]:
        print ('您要查询天气的位置为: {}{}{}市'.format(country, province, county))
    else:
        print ('您要查询天气的位置为: {}{}{}{}市'.format(country, province, city, county))

    text_info = ['当前天气为：{}'.format(text),'当前为气温: {}摄氏度'.format(temp), '当前湿度为: {}'.format(rh), '当前体感温度为: {}'.format(feels_like),
    '当前风向为: {}'.format(wind_dir), '当前风力为: {}级'.format(wind_class)]
    currnet = "当前天气为：{}\n当前为气温: {}摄氏度\n当前湿度为: {}\n当前体感温度为: {}\n当前风向为: {}\n当前风力为: {}级".format(
        text, temp, rh, feels_like, wind_dir, wind_class)
    for i in text_info:
        # print (i)
        pass
    """
    下面是解析未来几天的天气信息
    """
    all_info = ""
    for i in futrue:
        text_day = i['text_day']
        text_night = i['text_night']
        high = i['high']
        low = i['low']
        wc_day = i['wc_day']
        wd_day = i['wd_day']
        wc_night = i['wc_night']
        wd_night = i['wd_night']
        date = i['date']
        week = i['week']

        info = "日期：{} {} \n白天天气: {}\n晚上天气: {}\n最高气温: {}摄氏度\n最低气温: {}摄氏度\n白天风力: {}\n白天风向: {}\n晚上风力: {}\n晚上风向： {}".format(date, week,
                    text_day, text_night, high, low, wc_day, wd_day, wc_night, wd_night)
        futrue_info = ['日期：{}'.format(date), week, '白天天气: {}'.format(text_day), '晚上天气: {}'.format(text_night), '最高气温: {}摄氏度'.format(high),
        '最低气温: {}摄氏度'.format(low), '白天风力: {}'.format(wc_day), '白天风向: {}'.format(wd_day), '晚上风力: {}'.format(wc_night), '晚上风向： {}'.format(wd_night)]
        # print("#"*20)
        if all_info == '':
            all_info = "#"*30 + '\n' + info
        else:
            all_info = all_info + '\n' + "#"*30 + '\n' + info
        for i in futrue_info:
            # print (i)
            pass
    return currnet + '\n' + all_info 
    # return "我喜欢紧紧抱住你的那一刻，就像得到了全世界！"

def select():
    zh = is_chinese()
    if zh == 'True':
        print(P_info())
        try:
            return P_info()
        except:
            return "NameError: 您输入的城市名字有误......."
    else:
        return 'NaMeError: 请输入中文名.............'

def get_love():
    # 获取土味情话接口，第一个url为https://www.tianapi.com/console/上申请接口，每天只能调用100次
    # 平台账号: tjf0081 密码: WJ1996874353
    love_url1 = "http://api.tianapi.com/txapi/saylove/index?key=d22686670f6a1806f19c4172e279393a"
    love_url2 = "https://chp.shadiao.app/api.php"
    payload = {}
    headers = {}
    response = requests.request("GET", love_url1, headers=headers, data=payload)
    info = ''
    if response.status_code == 200:
        try:
            info = response.json()['newslist'][0]['content']
        except:
            pass                                                                            
    if info != "":                                                                                            
        return info                                                                                                 
    else:           
        response2 = requests.request("GET", love_url2, headers=headers, data=payload)
        if response2.status_code == 200:                                                                        
             return response2.text
        else:
            return "我喜欢紧紧抱住你的那一刻，就像得到了全世界！"

def main():
    s1 =select()
    # print (s1)
    #P_info()
    # import sed_email2
    from utils import sed_email2
    # sed_email2.sed_email(s1, ["hermantang@easyops.cn"], "天气预报")
    if "NaMeError" not in s1:
        message = s1 + '\n' + get_love()
        sed_email2.sed_email(message, ["hermantang@easyops.cn"], "天气预报")
    else:
        print(s1)

if __name__ == "__main__":
    s1 =select()
    # print (s1)
    #P_info()
    # import sed_email2
    from utils import sed_email2
    sed_email2.sed_email(s1, ["hermantang@easyops.cn"], "天气预报")
