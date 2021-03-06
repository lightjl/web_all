import os 
import sys
sys.path.append('..')

from lxml import etree
import requests
import time
import logging
from selenium import webdriver
from pydoc import browse
from multiprocessing import Process, Value
import threading

from common.sendMail import imMail
from moivesDownload.models import Moive, People, Watch, Statue_dm
from django.http import HttpResponse
import account
from common.baiduPan import bdpan

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')

    
def overDownloadNum(browser):
    time.sleep(4)
    try:
        browser.find_element_by_xpath('//div[@id="downloadVerify"]/div[1]')
        return True
    except:
        return False

def dowithDownload(status, moive, downloadDmSuccess, downloadDmFail):
    
    w = Watch.objects.filter(people__name="me", moive__name_En=moive.name_En)[0]
    if (status.text == '下载成功'):
        logging.info('下载成功')
        w.statue = downloadDmSuccess
        w.save()
        return  moive.name_En + '下载成功\r\n'
    else:
        w.statue = downloadDmFail
        w.save()
        browser.find_element_by_xpath('//*[@id="OfflineListView"]/dd[1]/div[4]/a[4]').click()    #取消下载
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="confirm"]/div[3]/a[1]/span').click()
        time.sleep(4)
        # //*[@id="confirm"]/div[3]/a[1]/span
        return moive.name_En + '下载失败\r\n'

def startBrower():
    browser = webdriver.Firefox()
    mypan = bdpan.BaiduPan(browser)
    mypan.login()
    #input('login youself!')
    browser.get('https://pan.baidu.com/disk/home?#/all?vmode=list&path=%2Fmoive')
    mypan.knowButtonClick()
    # 离线下载
    browser.find_element_by_xpath('//a[@data-button-id="b35"]').click()
    return browser

def downloadLink(browser, link):
    if link.startswith('ed2k'):   # ed2k
        time.sleep(4)
        # 新建链接
        browser.find_element_by_xpath('//*[@id="_disk_id_2"]/span/span').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="share-offline-link"]').send_keys(link)
        browser.find_element_by_xpath('//*[@id="newoffline-dialog"]/div[3]/a[2]').click()

        time.sleep(6)
        # //*[@id="OfflineListView"]/dd[1]/div[3]/span[2]
        status = browser.find_element_by_xpath('//*[@id="OfflineListView"]/dd[1]/div[3]/span[2]')
    elif link.startswith('magnet'):   # magnet
        time.sleep(4)
        # 新建链接
        browser.find_element_by_xpath('//*[@id="_disk_id_2"]/span/span').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="share-offline-link"]').send_keys(link)
        browser.find_element_by_xpath('//*[@id="newoffline-dialog"]/div[3]/a[2]').click()
        time.sleep(9)
        browser.find_element_by_xpath('//*[@id="offlinebtlist-dialog"]/div[3]/a[2]/span').click()

        time.sleep(6)
        # //*[@id="OfflineListView"]/dd[1]/div[3]/span[2]
        status = browser.find_element_by_xpath('//*[@id="OfflineListView"]/dd[1]/div[3]/span[2]')
        # 下载情况处理
    return status

def downloadbd(request):
    moives = Moive.objects.filter(watch__people__name="me", watch__statue__means="要下载")
    for mv in moives:
        logging.debug(mv.name_En + ' ' + mv.downloadLink)
    if (len(moives)==0):
        return HttpResponse("no mv to download")
    browser = startBrower()
    downloadDmSuccess = Statue_dm.objects.filter(means="在百度云")[0]
    downloadDmFail = Statue_dm.objects.filter(means="百度下载失败")[0]
    showText = ''
    for moive in moives:
        status = downloadLink(browser, moive.downloadLink)
         # 下载情况处理
        showText += dowithDownload(status, moive, downloadDmSuccess, downloadDmFail)
    browser.quit()
    return HttpResponse(showText)
        
    '''
    # link
    downloadLink = 'ed2k://|file|%E4%BC%A0%E8%AF%B4.Lore.S01E01.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.WEBrip.720p-%E4%BA%BA%E4%BA%BA%E5%BD%B1%E8%A7%86.mp4|481675554|046d15504c1a4488b5b7f7ce16a5478d|h=e6ljvcib5pwu6v44zf5tl3ycdbjzfdnw|/'
    browser.find_element_by_xpath('//*[@id="share-offline-link"]').send_keys(downloadLink)
    browser.find_element_by_xpath('//*[@id="newoffline-dialog"]/div[3]/a[2]').click()
    time.sleep(9)
    # //*[@id="OfflineListView"]/dd[1]/div[3]/span[2]
    status = browser.find_element_by_xpath('//*[@id="OfflineListView"]/dd[1]/div[3]/span[2]')
    if (status.text == '下载成功'):
        logging.info('下载成功')
    # //*[@id="OfflineListView"]/dd[1]/div[3]/span[2] == '下载中' or '下载成功'
    # //*[@id="OfflineListView"]/dd[2]/div[3]/span[2] 
    '''

def downloadLocal(link):
    browser = startBrower()
    print(downloadLink(browser, link))
    browser.quit()
    
if __name__ == "__main__":
    link = 'ed2k://|file|神盾局特工.Marvels.Agents.of.S.H.I.E.L.D.S05E13.中英字幕.HDTVrip.720P-人人影视.mp4|505753085|d92492963357cbe25465c881c45b73a2|h=ijf6i2hoakg4moh5ewkqap7vdeqdtcas|/'
    downloadLocal(link)
