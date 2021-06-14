import requests
import os
import random
import agent_headers
header = random.choice(agent_headers.USER_AGENTS)
headers = {
    "user-agen": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "sec-fetch-site": "same-origin",
    "path": "/artist?id=5781",
    "referer": "https://music.163.com/",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "pgrade-insecure-requests": "1",
    "scheme": "https",
    'authority': 'music.163.com',
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cookie": "nts_mail_user=tjf19968743@163.com:-1:1; mail_psc_fingerprint=c5571dd19b789ab6b22c89123fe68d7c; _iuqxldmzr_=32; _ntes_nnid=22e004534f8a1fd00d13dc804eaef077,1606322585790; _ntes_nuid=22e004534f8a1fd00d13dc804eaef077; NMTID=00O7JWyeRonS-MalEjtk2vGRv_SiDsAAAF2AEmCWQ; WM_TID=3ZRR1vYo1G9FFQFRVQdvcrapzOrc3o4W; WEVNSM=1.0.0; WNMCID=dpfseq.1619102221774.01.0; playerid=30303120; NTES_SESS=nOjw0SjDTkdGkqiO5y.IagYF_ohm.NrvXxVrTbgkiWvm3iTX3xgZlsyO8ZLrm1Z2lkt.rXeDfTu4t66GNJ8P607uwLELaBLP7N8WgLL_ILi9NyatIiccGRG6MPnE607w8zmwDHVh325LoU2UzTygawwLMTBDy.8yjfdHbsjMQAfW0om1_gHlJ_RXei_tDmguMX9IIxGXpWGYs; S_INFO=1619707547|0|3&80##|tjf19968743; P_INFO=tjf19968743@163.com|1619707547|0|mail163|00&99|gud&1618415122&mail163#gud&440300#10#0#0|&0||tjf19968743@163.com; playliststatus=visible; WM_NI=olHIABEAubCfh21sORU80sefLYJ3JZEHPdGTE%2F%2Biv16%2Bj5xVNdOEoqKk9KRm7Ibf7HikuxCX76FvUUI4q9Yo63Klvyvl6948dmsTzTF3h2MaHPNfPCmAMKykcXLYwgvuMzU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb4f27aaf899790ae68948e8bb2d84f878e8baef161b5bbbca7ed7aade8b8d4f92af0fea7c3b92aadb488aac44a879fbb83c26eaceeff94ce5a97e80094e86e908786d4c9528798a085c66087f1e58af53bf6f5a6d6fb5e8ebc81a6ee7b89b5f7acd167f597ae87b644abb5bb99c254f5ea8a97d85f8becbfdadc65f6ed858df573b6b4fadab734a8b3bdb5f96086eda8d3d06b8c908287d349af9f83acfc61a18884baf66db6ab839bd837e2a3; MUSIC_EMAIL_U=55daec99a3fe9a62710450bd889c74581a76b2fa248a2b858b902793aa507c332db24eb10ec4c07b33a649814e309366; BOX_DISABLE=true; csrfToken=b6SSorf8AFGZ24_RW7Uj5KUK; JSESSIONID-WYYY=Dlh1buxGuDVol5DnR9eXUsd9jMnq0Z6nZ%5CBbBIsDXDZZcZyqaGjWJ4RqibrIFhjAKc5BjB%2FTFjei5aWyOmyot1P%2BmsYnNf4HMOEwsslxpaIQyi%5CilP%5CgqEUqmGw7dMXqOahYJX07sq6bQWVmy9IFvnlgwD9EqFzER5fdBggJZiDy%5CNDX%3A1619777720939; __remember_me=true; __csrf=16598bf5e795219f5bbe159c9fb13b2f; MUSIC_U=55daec99a3fe9a62710450bd889c74581a76b2fa248a2b858b902793aa507c33c3990b790573715c33a649814e309366"
}
data= {
"id": 5781
}
sesscon = requests.Session()
def get_html(url):
    response = sesscon.get(url, headers=headers,data=data)
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
def post_html(url, data):
    response = sesscon.post(url, data, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response
    else:
        print(response)

def main():
    # url = "https://m701.music.126.net/20210423232848/a002b0c1f30dab7ba41c84a1b997fe60/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/5290124176/fb72/1fe5/79db/3fc4d57553dc1e6d53b623fba5b45401.m4a"
    # wget_file(url, 'test1.m4a')
    # p_url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
    # data = {
    #     "params": "TSenU6AW0R/DjzKuHR7zXVj4WRocW/L9OioF4kCThiGZXQWWA+FYsfI0MwaOsnmgoOGfEiXNNlAOz7OVDQc3WBKdV3Y7UfMIzEYgTeXUqnAr+DSHEXyfrL/CUEfdoKw1akqhRbW5ItyuqFoY+aCS5Q==",
    #     "encSecKey": "8ad70979f9b59a2bf70624fbd24b6ba86e8b27141e4ef16e1c171a3736cba4e246c1b1da94446972ed8bec92184c72170f0fe04bc6bea40c0e048147909b094771b2c92f52a6d4a4c8ef45f383a43130f566c831e1708641f319e0f78201792fc7ce35fcc0ae7646740f5380c8f673a5e05be8e5341921dab3d5555c1220e4a9"
    # }
    # post_html(p_url, data)
    # a = "http://s3.music.126.net/web/s/core_687747eaea35bc72e6e87b61c45d64b8.js?687747eaea35bc72e6e87b61c45d64b8.m4a"
    # c = "http://m801.music.126.net/20210423234300/44d31b12f4a6bbcb4e65872714adfab1/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/7384713590/457e/8dff/b4f2/a6069ebed4f59b7187cf6131af2b0b78.m4a"
    _url = "https://music.163.com/#/artist?id=5781"
    # _url= "https://music.163.com/"
    wget_file(_url, "test.html")

if __name__ == '__main__':
    main()