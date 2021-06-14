# encoding: utf-8
# data: 2021-06-04
#
import requests
from lxml import etree
import agent_headers
import random
ip = ":8080"

url = "https://www.xbiquge.la/modules/article/waps.php"
# headers = {
#     "user-agen": random.choice(agent_headers.USER_AGENTS),
#     "Cookie": "BAIDU_SSP_lcr=https://www.baidu.com/link?url=aB0gyB6-GoFZkrL746TCWvSadRrap33bPmPMU1yUmO7&wd=&eqid=f8ae79b90005bbcf0000000660b9ddd5; _abcde_qweasd=0; Hm_lvt_169609146ffe5972484b0957bd1b46d6=1622793693; cscpvrich9192_fidx=1; cscpvcouplet9193_fidx=1; Hm_lpvt_169609146ffe5972484b0957bd1b46d6=1622793731"
# }
headers = {
    "user-agen": random.choice(agent_headers.USER_AGENTS)

}
payload = {
    "searchkey": "雪中悍刀行"
}
data = {}
def get_ip():
    response = requests.get(
        "http://api.wandoudl.com/api/ip?app_key=757dd09465709402917c94545fb62d33&pack=0&num=20&xy=1&type=2&lb=\r\n&mr=1&area_id=undefined")
    proxies_list = []
    if response.status_code ==200:
        response = response.json()['data']
        for i in response:
            ip = i['ip']
            post = i['port']
            proxy = "http://{}:{}".format(ip, post)
            dict1 = {}
            dict1['http'] = proxy
            proxies_list.append(dict1)
    return proxies_list
proxies_list = get_ip()
sesscon = requests.Session()
def get_html(url):
    response = sesscon.get(url, headers=headers, data=data, proxies=random.choice(proxies_list))
    if response.status_code == 200:
        return response
    else:
        print("Error: get html failed")

def post_html(url):
    response = sesscon.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response
    else:
        print("Error: get html failed")

def wget_file(url, file_path):
    response = get_html(url)
    if response != None:
        with open(file_path, 'wb') as f:
            f.write(response.content)
            f.close()

def get_contents_urls(book_url):
    book_url_dict = {}
    contents_response = get_html(book_url).content
    contents_tree = etree.HTML(contents_response)
    content_url_list = contents_tree.xpath('//div[@class="box_con"]/div[@id="list"]/dl/dd/a/@href')
    chapter_name_list = []
    for i in content_url_list:
        chapter_name = contents_tree.xpath('//div[@class="box_con"]/div[@id="list"]/dl/dd/a[@href="{}"]/text()'.format(i))[0]
        url = book_url + i.split('/')[-1]
        book_url_dict[chapter_name] = url
        chapter_name_list.append(chapter_name)
    return chapter_name_list, book_url_dict

def save_book(chapter_name_list, book_url_dict, book_path):
    # print(chapter_name_list)
    with open(book_path, 'wb') as f:
        for name in chapter_name_list:
            if name in book_url_dict.keys():
                print(name)
                f.write(str(name).encode())
                url = book_url_dict[name]
                print(url)
                response = get_html(url)
                if response != None:
                    url_tree = etree.HTML(response.content)
                    contents = url_tree.xpath('//div[@id="content"]/text()')
                    print(contents)
                    for i in contents:
                        f.write(str(i).encode())
                    # exit()
                f.write('\n\n'.encode())
    f.close()


def main():
    response = post_html(url)
    if response != None:
        html = response.content
        tree = etree.HTML(html)
        books_tree = tree.xpath('//td[@class="even"]/a/@href')
        book_dict = {}
        book_name_list = []
        if books_tree != []:
            for book_url in books_tree:
                book_name = tree.xpath('//td[@class="even"]/a[@href="{}"]/text()'.format(book_url))[0]
                book_dict[book_name] = book_url
                book_name_list.append(book_name)
                chapter_name_list, book_url_dict = get_contents_urls(book_url)
                save_book(chapter_name_list, book_url_dict, book_path="test.txt")



if __name__ == '__main__':
    # main()
    import os
    print(os.path.exists("test"))
    # print(os.mkdir("test"))
    # wget_file("https://www.xbiquge.la/0/745/", file_path="test.html")
    # x, y = get_contents_urls("https://www.xbiquge.la/0/745/")
    # a = "https://www.xbiquge.la/0/745/"
    # print(a.split('/'))
    # for i in x:
    #     print(i)
