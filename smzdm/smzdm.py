import time
import logging
from selenium import webdriver
import threading
import re
from django.http import HttpResponse
from smzdm.models import zdmSp, zdmWeb
from common.sendMail import sendMail
from email_os import p_email_os

def checkWeb(browser, url):
    browser.get(url)
    lis = browser.find_elements_by_xpath('//*[@id="feed-main-list"]/li')
    plus = False # 没京东plus会员
    email = p_email_os.Email_os()
    
    for li in lis:
        hwmc = (li.find_element_by_xpath('./div/div[2]/h5/a[1]').text)
        if (not plus) and ('PLUS' in hwmc):
            continue
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
        else:
            je = 0
        # print(yhStr)
        gxsj = (li.find_element_by_xpath('./div/div[2]/div[2]/div[2]/span').text)
        sps = zdmSp.objects.filter(hwmc=hwmc, gxsj=gxsj)
        if len(sps)>=1 :
            break
        sp = zdmSp(hwmc=hwmc, mj=mj, by=by, je=je, url=url, bz=yhStr, gxsj=gxsj)
        sp.save()
        if not ('-' in gxsj):
            txt = 'smzdm:' + hwmc + ' ' + str(je) + '\n' + yhStr + '\n' + url  # 邮件通知
            email.add_mail_item(subject='什么值得买', topic='什么值得买', txt=txt, minutes_delay=10, deadline=None, cover=False)

def checkAll():
    urls = zdmWeb.objects.filter(gxFlag = True)
    logging.critical(urls)
    browser = webdriver.Chrome()
    for url in urls:
         checkWeb(browser, url.url)
    browser.quit()

def smzdm(request):
    checkAll()
    showText = 'Checked'
    #check = threading.Thread(target=checkAll)
    #check.start()
    return HttpResponse(showText)