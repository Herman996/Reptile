# encoding: utf-8
import requests
from lxml import etree
import time
import openpyxl
import _thread
import threading
s = requests.Session()

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }

def get_html(url):
    cookie = "tradeMA=229; totalProdQty=0; _snsr=baidu.com%7Corganic%7C%7C%7C*%3A*; _snvd=1624096437209ho69Mv1YQaB; _snzwt=THnRgQ17a23b137e0mGun2b98; hm_guid=5b6070f0-81c0-4db8-9df3-35227929234e; cityId=9051; districtId=10346; _snmc=1; _snms=162412281531765376; authId=siZFiphi7ShjlyExCmZDDrRirLPd6POZTs; secureToken=01FF6D6D71AD2D07DD44101084F0FECF; SN_CITY=190_755_1000051_9051_01_10346_1_1_99_7550199; isScale=false; _df_ud=a0f5c363-2d6b-4c71-8b09-c5957b9e6abd; streetCode=7550199; smhst=822008671|0070067079a11876446746|0071290403a11263439015|0070167435a12097557994|0071290403a11901660746|0070167435; token=4d09e3f4-5c06-428f-845d-e04f104a71c2; _snma=1%7C162409643702020733%7C1624096437020%7C1624124267837%7C1624124289676%7C23%7C2; _snmp=162412428905516157; _snmb=162412281527829510%7C1624124289727%7C1624124289687%7C13"
    response = s.get(url, headers=headers)
    # response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None


def get_noe_sn(url):
    p = '?safp=d488778a.10038.resultsRblock.12&safc=prd.3.ssdln_502687_pro_pic01-1_0_0_11876446746_0071290403&safpn=10006.502687'
    _response = get_html(url)
    if _response != None:
        z_tree = etree.HTML(_response)
        # li_list = z_tree.xpath('.//ul[@class="clearfix"]/li')
        book_info_url = z_tree.xpath('.//div[@class="img-block"]/a[@target="_blank"]/@href')
        book_info_list = z_tree.xpath('.//ul[@class="clearfix"]/li')
        # for book_info in book_info_list:
        #     info = book_info.xpath('.//p[@class="sell-point"]/a/text()')[0]
        #     book_name = info.replace('\n', '')
            # price_1 = book_info.xpath('.//p[@class="prive-tag"]/emphasis/b/text()')
            # price_2 = book_info.xpath('.//p[@class="prive-tag"]/em')[0]
            # em_str = etree.tostring(price_2, encoding="utf-8")       # 获取部分html代码
            # print(price_1)
            # print(em_str)

            # price = "¥" + price_1 + price_2
            # print(book_name + price)
        print(len(book_info_list))
        for i in book_info_url:
            print("http:"+i + p)


def main():
    index_url = 'https://book.suning.com/'
    response = get_html(index_url)
    if response !=  None:
        tree = etree.HTML(response)
        dl_list = tree.xpath('//div[@class="menu-item"]/dl')
        z_z_list = tree.xpath('//div[@class="menu-sub"]')
        all_dl_info = []
        for dl in dl_list:
            dl_dict = {}
            dl_url = dl.xpath('.//dt/h3/a/@href')[0]
            d_title = dl.xpath('.//dt/h3/a/text()')[0]
            dd_list = dl.xpath('.//dd/a')
            dl_dict['dl_name'] = d_title
            dl_dict['dl_url'] = dl_url
            zl_list = []
            for dd in dd_list:
                zl_dict = {}
                z_url = dd.xpath('.//@href')[0]
                z_name = dd.xpath('.//text()')
                zl_dict["z_name"] = z_name
                zl_dict['z_url'] = z_url
                zl_list.append(zl_dict)
            dl_dict['zl_info'] = zl_list
            all_dl_info.append(dl_dict)
        all_info_list = []
        for z_z in z_z_list:  # 获取所以子类信息
            z_z_name = z_z.xpath('.//div[@class="submenu-left"]/p/a/text()')
            for i in range(1, len(z_z_name) + 1):
                z_dict = {}
                a_list = z_z.xpath('.//div[@class="submenu-left"]/ul[{}]/li/a'.format(i))
                info_list = []
                for a in range(len(a_list)):
                    a_dict = {}
                    a_info = a_list[a]
                    a_url = a_info.xpath('.//@href')[0]
                    a_dict[a_info.xpath('.//text()')[0]] = a_url
                    info_list.append(a_dict)
                z_dict[z_z_name[i - 1]] = info_list
                all_info_list.append(z_dict)
        for info in all_info_list:
            print(info)

if __name__ == '__main__':
    # main()
    book_url = 'https://list.suning.com/1-502687-0.html'
    # get_noe_sn(book_url)

    b_url = "http://product.suning.com/0071290403/12097557994.html?safp=d488778a.10038.resultsRblock.12&safc=prd.3.ssdln_502687_pro_pic01-1_0_0_11876446746_0071290403&safpn=10006.502687"
    response = get_html(b_url)
    print(response)
    z_tree = etree.HTML(response)
    b = z_tree.xpath('//span[@class="mainprice"]')
    print(b)