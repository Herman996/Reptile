# encoding: utf-8
import requests
import re
import random
import agent_headers


# 模拟一个cookie登陆
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #"Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "taihe_bi_sdk_uid=e3e7490d5d72eb0c707167eebd185c72; taihe_bi_sdk_session=db242a9bd4c06b5760fa0333dfc87e4a; anonymid=kpo31ooqv6wtca; Hm_lvt_ad6b0fd84f08dc70750c5ee6ba650172=1623159155,1623159166,1623159190,1623760819; Hm_lpvt_ad6b0fd84f08dc70750c5ee6ba650172=1623761117; LOCAL_STORAGE_KEY_RENREN_USER_BASIC_INFO=%7B%22userName%22%3A%22%u674E%u5C06%22%2C%22userId%22%3A976591406%2C%22headUrl%22%3A%22http%3A//img.xiaonei.com/photos/0/0/men_head.gif%22%2C%22secretKey%22%3A%22897004012e5cecaa94268a420995d289%22%2C%22sessionKey%22%3A%22T2O4q961k2QE33OJ%22%7D",
    "Host": "www.renren.com",
    "If-None-Match": 'W/"2c956-iEC/6Nk1/n7AWbTBQAIBbJV6G/Y"',
    "Referer": "http://www.renren.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
def get_html(url):
    headers['user-agent'] = random.choice(agent_headers.USER_AGENTS)
    # print(headers)
    response = requests.get(url, headers= headers)
    if response.status_code == 200:
        return response

def wget_file(url, file_path):
    """
    将获取到的html页面代码写入到文件中
    :param url:         网页url
    :param file_path:   文件存放路径
    :return:            无
    """
    response = get_html(url)
    if response != None:
        with open(file_path, 'wb') as f:
            f.write(response.content)
            f.close()


if __name__ == '__main__':
    _url = "http://www.renren.com/"
    # print(get_html(_url))
    wget_file(_url, "test.html")
