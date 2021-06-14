# encoding: utf-8
# data: 2021-06-08
# author: HermanTang

import requests
from lxml import etree
import agent_headers
import random
import re
import os

headers = {
    "user-agen": random.choice(agent_headers.USER_AGENTS)

}
sesscon = requests.Session()
def get_html(url):
    response = sesscon.get(url, headers=headers,data={})
    if response.status_code == 200:
        return response
    else:
        print("Error: get html failed")


def analy_qq_html():
    _url = "https://pvp.qq.com/web201605/herolist.shtml"        # 王者荣耀官网首页
    response = get_html(_url)
    tree = etree.HTML(response.content)
    url_dict = {}
    img_url_list = tree.xpath('//ul[@class="herolist clearfix"]/li/a/@href')        # 获取到所有英雄详情界面的url
    for url in img_url_list:        # 通过循环取出每个英雄的名字与url进行拼接，得到字典{"英雄名": "详情页url"}
        url_dict[tree.xpath('//ul[@class="herolist clearfix"]/li/a[@href="{}"]/text()'.format(url))[0]] = "https://pvp.qq.com/web201605/" + url
    hero_name = url_dict.keys()
    if os.path.exists("../imgs") == False:      # 创建存放图片的imgs目录，首先判断文件是否存在，不存在则创建
        os.mkdir('../imgs')
    for name in hero_name:                      # 遍历出每个英雄以及对应的url
        hero_url = url_dict[name]
        hero_response = get_html(hero_url)      # 获取英雄详情页url
        hero_tree = etree.HTML(hero_response.content)       # 创建一个xpath对象
        hero_img_url = hero_tree.xpath('//div[@class="zk-con1 zk-con"]/@style')[0]      # 解析出详情页中的海报的url
        h_url = "http:" + re.match(r'background:url\(\'(.*)\'\)(.*)', hero_img_url).group(1)        # 再通过正则匹配到海报url
        file_path = '../imgs/' + name + ".jpg"                  # 定义影响图片的名字，这里表示上一个目录下imgs目录下
        img_response = get_html(h_url).content                  # 再通过海报url获取到海报的图片
        count = 1
        with open(file_path, 'wb') as f:                        # 将海报图片写入保存到本地
            f.write(img_response)
            f.close()
            print("第{}张图片：{}.jpg下载完成".format(count, name))
            count +=1

if __name__ == '__main__':
    analy_qq_html()
