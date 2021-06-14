# encoding: utf-8
import requests
from lxml import etree


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}
def get_url(name):
    _url = "https://v.qq.com/x/search/?q={}".format(name)
    response = requests.get(_url)
    if response.status_code == 200:
        tree = etree.HTML(response.text)
        # movie_url = tree.xpath('//div[@class="result_btn_line"]/a[1]/@href')
        movie_url = tree.xpath('//div[@class="result_btn_line"]/a[1]/@href')
        print(movie_url)

def get_pm4():
    _url = "https://ltsbsy.qq.com/uwMROfz2r5zAoaQXGdGnC2df644E7D3uP8M8pmtgwsRK9nEL/EjVU6R-gnZi-CJGVHCxGe9rSlK0_Saa5RHxSQdrXQHMW44A4Tu7-683u6gIwmjPP9pp2PCfVmXTBfWzu65MYQlzuNzNGzIE23FqiW5p5lEiN0_SZ4Zsq_KX0wrswaHC47v5npMdGg4wvepy25Q8eRze8deaaAJB3pq2q28ZFKaQ/029_u0019euozko.321002.2.ts"
    response = requests.get(_url, headers=headers)
    print(response.text)
    if response.status_code == 200:
        print(response.content)
        with open('gtx.mp4', 'wb') as f:
            f.write(response.content)
            f.close()



if __name__ == '__main__':
    # get_url("钢铁侠")
    # get_pm4()
    file = open('main.py')
    while 1:
        filne = file.readline()
        print(filne)
        if not filne:
            break