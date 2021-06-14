# encoding: utf-8

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

def login():
    _url = "http://www.qianmu.org/login"
    data = {
        "mobile": "18108441775",
        "psd": "123456"
    }
    response = sesscon.request(method="POST", url=_url, headers=headers)
    return response


def get_html(url):
    response = sesscon.get(url, headers=headers,data={})
    if response.status_code == 200:
        return response
    else:
        print("Error: get html failed")


def analy_school():
    login()
    url = "http://www.qianmu.org/ranking/1528.htm"
    index_response = get_html(url)
    school_dict = {}
    schools = []
    if index_response.status_code == 200:
        tree = etree.HTML(index_response.content)
        school_url_list = tree.xpath('//td[@style="outline: 0px !important;"]/a/@href')
        for school in school_url_list:
            school_name = tree.xpath('//td[@style="outline: 0px !important;"]/a[@href="{}"]/text()'.format(school))
            if school_name != []:
                school_dict[school_name[0]] = school
                schools.append(school_name[0])
        # print(school_url_list)
    print(school_dict)
    print(schools)
    for s in schools:
        s_url = school_dict[s]
        school_response = get_html(s_url)
        if school_response.status_code == 200:
            sch_tree = etree.HTML(school_response.content)
            # tr_list1 = sch_tree.xpath('//div[@class="wikiContent"]/div/table/tbody/tr/td[1]/p[1]//text()')
            # tr_list2 = sch_tree.xpath('//div[@class="wikiContent"]/div/table/tbody/tr/td[2]/p[1]//text()')
            # print(len(sch_tree.xpath('//div[@class="wikiContent"]/div/table/tbody/tr')))
            # print(tr_list1)
            # print(tr_list2)
            # print(len(tr_list1))
            # print(len(tr_list2))
            for i in range(1, len(sch_tree.xpath('//div[@class="wikiContent"]/div/table/tbody/tr')) + 1):
                tr_list1 = sch_tree.xpath('//div[@class="wikiContent"]/div/table/tbody/tr[{}]/td[1]/p[1]//text()'.format(i))
                tr_list2 = sch_tree.xpath(
                    '//div[@class="wikiContent"]/div/table/tbody/tr[{}]/td[2]/p[1]//text()'.format(i))
                if tr_list1 != [] and tr_list2 != []:
                    print("{}:{}".format(tr_list1[0], tr_list2[0]))


            # tr = sch_tree.xpath('//div[@class="wikiContent"]/div/table/tbody/tr')
            # for i in tr:
            #     tb = i.xpath('./tr/tb')
            #     print(tb)
            exit()


if __name__ == '__main__':

    analy_school()
