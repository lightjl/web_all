import time
import logging
from selenium import webdriver
import threading
import re
from django.http import HttpResponse
from smzdm.models import zdmSp, zdmWeb


def checkWeb(browser, url):
    browser.get(url)
    lis = browser.find_elements_by_xpath('//*[@id="feed-main-list"]/li')
    for li in lis:
        hwmc = (li.find_element_by_xpath('./div/div[2]/h5/a[1]').text)
        url = (li.find_element_by_xpath('./div/div[2]/h5/a[1]').get_attribute("href"))
        yhStr = li.find_element_by_xpath('./div/div[2]/h5/a[2]/div').text
        if '满' in yhStr:
            mj = True
        else:
            mj = False
        if '包邮' in yhStr:
            by = True
        else:
            by = False
        price = re.search('[.0-9]*元', yhStr)
        if price:
            je = float((price.group())[:-1])
        # print(yhStr)
        gxsj = (li.find_element_by_xpath('./div/div[2]/div[2]/div[2]/span').text)
        sps = zdmSp.objects.filter(hwmc=hwmc, gxsj=gxsj)
        if len(sps)>=1 :
            break
        sp = zdmSp(hwmc=hwmc, mj=mj, by=by, je=je, url=url, bz=yhStr, gxsj=gxsj)
        sp.save()

def checkAll():
    urls = zdmWeb.objects.all()
    browser = webdriver.Firefox()
    for url in urls:
         checkWeb(browser, url.url)

def smzdm(request):
    checkAll()
    showText = 'Checked'
    #check = threading.Thread(target=checkAll)
    #check.start()
    return HttpResponse(showText)