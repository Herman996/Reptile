# encoding: utf-8
import requests
from lxml import etree
import time
import openpyxl
import _thread
import threading


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
def get_html(url):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        return None

def write_execl(start, info_list, n):
    # start = start +2
    # print(start)
    s = 1
    for i in info_list:
        # print(i)
        table['A{}'.format(start)] = start-1
        table['B{}'.format(start)] = i['PostId']
        table['C{}'.format(start)] = i['RecruitPostName']
        table['D{}'.format(start)] = i['CountryName']
        table['E{}'.format(start)] = i['LocationName']
        table['F{}'.format(start)] = i['Responsibility']
        table['G{}'.format(start)] = i['CategoryName']
        table['H{}'.format(start)] = i['LastUpdateTime']
        p_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId={}".format(i['PostId'])
        p_response = get_html(p_url)
        # print(p_response)
        Requirement = ''
        if p_response:
            p_posrt_info = p_response.json()['Data']
            if "Requirement" in p_posrt_info.keys():
                Requirement = p_posrt_info["Requirement"]  # 职位要求
        table['J{}'.format(start)] = p_url
        table['I{}'.format(start)] = Requirement
        # print(start)
        start +=1
        print("数据{}已经写入到第{}条数据".format(n, s))
        s +=1

if __name__ == '__main__':
    url = "https://careers.tencent.com/tencentcareer/api/post/Query?&pageIndex=1&pageSize=10000"
    file_path = "tencent.xlsx"
    response = get_html(url)
    # print(response.json())
    Data = response.json()['Data']
    Posts = Data['Posts']
    wb = openpyxl.Workbook()
    table = wb.create_sheet(u"工具列表", 0)
    row = 2  # 行
    table['A1'] = '序号'
    table['B1'] = '职位ID'
    table['C1'] = '职位名称'
    table['D1'] = '职位所在国家'
    table['E1'] = '职位所在市'
    table['F1'] = '岗位职责'
    table['G1'] = '岗位分类'
    table['H1'] = '发布时间'
    table['I1'] = '职位要求'
    table['J1'] = '招聘URL'
    count = len(Posts)
    write_execl(2, Posts, count)
    # print(count)
    # c = count//1
    # start = 0
    # end = c
    # t1 = threading.Thread(target=write_execl, args=(2,Posts, 1))
    # t1.start()
    # for i in range(1):
    #     if i == 9:
    #         end = -1
    #     # print("{}-{}".format(start, end))
    #     info_list = Posts[start:end]
    #     # print(info_list)
    #     # print(info_list)
    #     t1 = threading.Thread(target=write_execl, args=())
    #     try:
    #         _thread.start_new_thread(write_execl, (start+2, info_list, i+1,))
    #         # _thread.start_new_thread(write_execl, ("Thread-2", 4,))
    #     except:
    #         print("Error: 无法启动线程")
    #     start = end
    #     end = c + end
    wb.save(file_path)



