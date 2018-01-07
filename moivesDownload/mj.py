import sys
sys.path.append('..')
import requests
from bs4 import BeautifulSoup
import re
from common import WorkInTime
from moivesDownload import account
from moivesDownload import moiveE
from lxml import etree
import logging
import time
from multiprocessing import Process, Value
import threading
import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

@csrf_exempt 
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
    time.sleep(5)
    f = login_session.get(url)
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
            name = moive.xpath('./a[1]/span/text()')[0]
            link = moive.xpath('./div/div/div/a[2]/@href')[0]
            mv = moiveE.moiveE(name, link)
            myMoives.send(mv)
            # print(moive.xpath('./a[1]/span/text()')[0])
            # print(moive.xpath('./div/div/div/a[2]/@href')[0])
    # print(f.content.decode())

    # logging.critical('well done')
    return HttpResponse("well done")

runFlag = Value('b', True)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/mj.pyrunable.txt'
    file_object = open(filename, 'r')
    try:
        flag_run = file_object.read()
    finally:
        file_object.close()
    while flag_run == 'True':
        time.sleep(5)
        file_object = open(filename, 'r')
        try:
            flag_run = file_object.read()
        finally:
            file_object.close()
    runFlag.value = False
    


if __name__ == '__main__':
    # 检查是否要运行
    checkRun = threading.Thread(target=checkRunFlag, args=())
    checkRun.start()
    timeBucket =[['7:00', '7:6'], ['9:00', '9:6'], ['12:00', '12:10'], ['18:00', '18:06']]
    
    workTime = WorkInTime.WorkInTime(timeBucket, relaxTime=60*10)
    logging.critical("following mv")
    remindThread = threading.Thread(target=remind.remind)
    remindThread.start()
    # while True:
        #downloaded = checkDownloaded.checkDownloaded()
    while runFlag.value:
        loginAndDownload()
        relaxNow = threading.Thread(target=workTime.relax, args=(runFlag,))
        relaxNow.start()
        relaxNow.join()
    # workTime.relax()
