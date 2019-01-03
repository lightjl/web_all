from lxml import etree
import requests
from common.sendMail import sendMail
from common.sendMail import recMail
import time
import datetime
import threading
import logging
from common.sendMail import imMail
from followXS.models import Xs, Chapter
from common.saveFile import saveTxt
from email_os import p_email_os


#timeB = [['19:46', '23:00']]

class XS:
    def __init__(self, id):
        self.xs = Xs.objects.get(id=id)
        self.name = self.xs.rask.name
        self.__url = self.xs.url
        self.__getContent = saveTxt.saveToFile('xs')
        self.email = p_email_os.Email_os()

    def getUrl(self):
        return self.__url

    def save(self, filename, text, size=5):
        return self.__getContent.save(filename, text, size)

    def sendToKindle(self, filename, url=''):
        sendHotmail = threading.Thread(target=sendMail.sendMail, args=(filename, \
                'xs:'+filename+'\n'+url, 'ming188199@hotmail.com', 'hotmail', False))
        
        # sendMail.sendMail(filename, 'xs:'+filename, receiver='ming188199@hotmail.com', sendFrom='hotmail')
        self.email.add_mail_item(subject='小说', topic=filename, txt='xs:'+filename+'\n'+url, minutes_delay=30, deadline=None, cover=False)
        if '第' in filename:
            logging.debug("更新了"+filename)
            sendMail.send_attachment_kd(self.__getContent.getSavePath().joinpath(filename+'.txt'))
            
        # sendHotmail.start()

        
    def getZjName(self, webSite, zj):
        zjName = ''
        if webSite == '888':
            zjName =  (zj.xpath('./text()')[0])
        elif webSite == 'sodu':
            zjName =  (zj.xpath('./div[1]/a/text()')[0])
        if (zjName[-1] == '('):#（((
            zjName = zjName[:-1]
        zjName = zjName.split('（')[0]
        return zjName
        
    def getZjUrl(self, webSite, zj):
        if webSite == '888':
            return (zj.xpath('./@href')[0])
        elif webSite == 'sodu':
            zjHref = zj.xpath('./div[1]/a/@href')[0]
            return zjHref.split('url=')[1]
        
    def doWith_zj(self, zjs, zjUrlHead, webSite):
        for zj in zjs:
            # /html/body/div[6]/div[1]/a
            zjName = self.getZjName(webSite, zj)
            # print(zjName)

            zjHref = zjUrlHead + self.getZjUrl(webSite, zj)
            # print(zjHref)
            zjs = Chapter.objects.filter(xs=self.xs, name=zjName)
            if (len(zjs)==0):
                try:
                    html = requests.get(zjHref)
                except:
                    continue
                html.encoding = 'utf-8'
                selector = etree.HTML(html.content)

                divs = (selector.xpath('//div[@id]'))
                text = ''
                for div in divs:
                    id = (div.xpath('@id'))[0]
                    if id == 'content' or id == 'contents' or id == 'txtContent' or id == 'BookText':
                        # print(div.xpath('//text()'))
                        for eachP in (div.xpath('./text()')):
                            text += eachP + '\r\n'

                # print(text)
                if len(text) > 89:     # 避免下载空文件
                    #ss = threading.Thread(target=self.sendShouqu, args=(zjHref,))
                    #ss.start()
                    if (self.save(zjName, text, 5)): # 小说章节大于5KB才正常
                        self.sendToKindle(zjName, zjHref)
                        cp = Chapter(xs=self.xs, name=zjName)
                        cp.save()  # 送出后更新
                    elif '第' not in zjName: # 非小说章节
                        self.sendToKindle(zjName, zjHref)
                        cp = Chapter(xs=self.xs, name=zjName)
                        cp.save()  # 送出后更新
        
    def sodu888(self, selector):
        zjs = selector.xpath('//a[@rel="nofollow"]')
        zjUrlHead = 'http://www.sodu888.com'
        # print(zjs)
        self.doWith_zj(zjs, zjUrlHead, '888')
                    
                    
    def sodu(self, selector):
        zjs = selector.xpath('//div[@class="main-html"]')
        zjUrlHead = ''
        self.doWith_zj(zjs, zjUrlHead, 'sodu')
        
        
    def follow(self):
        #logging.info('checking' + self.name)
        # logging.critical(self.getUrl())
        try:
            url = self.getUrl()
            html = requests.get(url, timeout = 1)
            selector = etree.HTML(html.text)
        except:
            return
        #print(html.text)
        
        #zjs = selector.xpath('//a[@rel="nofollow"]/text()')
        #print(zjs)

        # /html/body/div[6]
        logging.critical("following " + self.name)
        if ("cc" in self.name):
            self.sodu(selector)
        elif("sodu3" in url or "sodu888" in url):
            self.sodu888(selector)
            
                