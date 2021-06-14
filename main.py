# encoding: utf-8
import requests
from lxml import etree
"""
爬取熊猫办公
"""
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

def wget_mp4(url):
    pass

def copy_mp4(file_name, new_file_name):
    # 视频复制
    import time
    # 开始时间
    start_time = time.time()
    # 以二进制方式打开视频
    v_src = open(file_name, 'rb')
    # 读取视频中所有数据
    content = v_src.read()
    # 创建复制出来的文件
    v_copy = open(new_file_name, 'wb')
    # 写入
    v_copy.write(content)
    # 关闭操作
    v_src.close()
    v_copy.close()
    # 结束时间
    end_time = time.time()
    print('耗时：', (end_time - start_time))


def main():
    _url = "https://www.tukuppt.com/muban/lvvvozep.html"
    response = get_html(_url)
    # print(response)
    if response != None:
        tree = etree.HTML(response)
        videos_url = "https:" + tree.xpath('//video[@id="videoe"]/@src')[0]
        print(videos_url)
        mps_info = requests.get(videos_url).content
        print(mps_info)
        with open("test.mp4", 'wb') as f:
            f.write(mps_info)
            f.close()




if __name__ == '__main__':
    # main()
    _url = "https://btrace.video.qq.com/kvcollect?BossId=3647&Pwd=1005892234&osVer=mac%2010.15.5"
    response = requests.get(_url).content
    print(response)