# encoding: utf-8
import requests
from lxml import etree
import time
# from utils import sed_email2
import sed_email2
# from 接口获取 import sed_email2

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
def get_html(url):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_info():
    """
    通过网页中的p标签的text文件中的日期判断是不是当天更新，通过下标获取到对应的网页url，
    注意：xpath中的下标是以1开始，所以在获取到的时间的下标的基础上加1
    再获取新闻网页的源码进行解析，获取新闻简报
    """
    _url = "https://www.163.com/dy/media/T1603594732083.html"
    response = get_html(_url)
    info = ""
    if response != None:
        tree = etree.HTML(response)     # 创建xpath对象
        time_list = tree.xpath('//div/p[@class="media_article_date"]/text()')       # 获取到所有的新闻网页url对应的更新时间
        currnet_time = str(time.strftime("%Y-%m-%d", time.localtime()))         # 获取当前的时间日期
        new_url = ''
        for t in time_list:
            if t.split(' ')[0] == currnet_time:
                new_url = tree.xpath('//ul[@class="media_articles_list"]/li[{}]/a/@href'.format(time_list.index(t) + 1))[0]     # 获取新闻的url
        # print(new_url)        # 打印新闻url
        if new_url == "":
            """
            这里是判断新闻的url是否为空，为空则代表解析失败
            """
            TO = ['hermantang@easyops.cn']
            info = "解析365新闻首页的url失败，无法获取当前日期的新闻url，请检查url【{}】".format(_url)
            sed_email2.sed_email(info, TO, "获取简报失败")
            # print("Error:获取简报失败！")
            exit()
        new_reposne = get_html(new_url)
        if new_reposne != None:
            tree1 = etree.HTML(new_reposne)
            # new_info = tree1.xpath('//div[@class="post_body"]/p[@class!="f_center"][1]//text()')
            new_info = tree1.xpath('//div[@class="post_body"]/p[not(contains(@class,"f_center"))]') # 获取匹配到的div标签下的p标签属性class不等于f_center的
            if len(new_info) > 3:
                br_info = new_info[1]
                br = br_info.xpath('.//text()')
            else:
                br = []
            # if '\u3000\u3000' in br:        # 删除解析新闻页面时多于的参数
            #     br.remove('\u3000\u3000')     # 可以不注释，这事清楚新闻开头的两行空行
            if len(br) > 0:
                for i in br:
                    # print(i)
                    if "今日早报——365资讯简报，" in i:
                        i = i.replace('今日早报——365资讯简报，', '')
                    if i not in info:
                        if info == "":
                            info = i
                        else:
                            info = info + '\n' + i
        else:
            info = "获取新闻页面时错误，url为【{}】".format(new_url)
    else:
        info = "请求365新闻首页失败，无法获取页面中信息【{}】".format(_url)
    return info
if __name__ == '__main__':
   # info = get_info()
   TO = ['hermantang@easyops.cn']
   SUBJECT = '每日简报'
   import get_weather
   # get_weather.main()
   info = get_info()
   if info != "":
       # pass
       sed_email2.sed_email(info, TO, SUBJECT)
