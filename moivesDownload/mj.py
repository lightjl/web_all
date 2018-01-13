import sys
sys.path.append('..')
import requests
from bs4 import BeautifulSoup
import re
import account
from moivesDownload import moiveE
from lxml import etree
import logging
import time
from multiprocessing import Process, Value
import threading
import os

from django.http import HttpResponse

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

 
def loginAndDownload(request):  # 登陆函数
    myMoives = moiveE.moives()
    header = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Origin':'http://www.zimuzu.tv',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    url = 'http://www.zimuzu.tv/User/Login/ajaxLogin'

    # postData="account=用户名&password=密码&remember=1"
    login_session = requests.Session()
    login_session.post(url,
           data=account.postData233,
           headers=header)
    _cookies = (login_session.cookies)
    #print(login_session.status_code)
    #print(_cookies.get_dict())
    url = 'http://www.zimuzu.tv/user/fav'
    f = login_session.get(url)
    time.sleep(5)
    selector = etree.HTML(f.text)
    # print(selector)
    ## /html/body/div[4]/div/div/div[2]/div/ul/li[1] /div[2]/ul/li[1] /a[1]/span
    # /html/body/div[4]/div/div/div[2]/div/ul/li[1] /div[2]/ul/li[1] /div/div/div/a[2]
    ## /html/body/div[4]/div/div/div[2]/div/ul/li[1]/div[2]/ul/li[2]/a[1]/span
    # /html/body/div[4]/div/div/div[2]/div/ul/li[1]/div[2]/ul/li[2]/div/div/div/a[2]
    
    # /html/body/div[4]/div/div/div[2]/div/ul/li[2]/div[2]/ul/li[1]/a[1]/span
    content_field = selector.xpath('//li[@class="clearfix"]')
    if (len(content_field) == 0):
        return HttpResponse("check mv failed!!!!!!!!!!!")
        myMoives.checkFailedNotice()
        runFlag.value = False
        
    for each in content_field:
        moives = each.xpath('./div[2]/ul/li')
        for moive in moives:
            try:
                name = moive.xpath('./a[1]/span/text()')[0]
                link = moive.xpath('./div/div/div/a[2]/@href')[0]
                mv = moiveE.moiveE(name, link)
                myMoives.send(mv)
                # print(moive.xpath('./a[1]/span/text()')[0])
                # print(moive.xpath('./div/div/div/a[2]/@href')[0])
            except:
                continue
    # print(f.content.decode())

    # logging.critical('well done')
    return HttpResponse("well done")

