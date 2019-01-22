from lxml import etree
import requests
from book.models import Book
from .doubanBook import DoubanBook
import datetime
from common.baiduPan import bdpan
from selenium import webdriver
import re

class BookDownloadInfo:
    def __init__(self, mebooklink):
        html = requests.get(mebooklink)
        selector = etree.HTML(html.text)
        download_selector = selector.xpath('//*[@id="content"]/div/p[6]/strong/a/@href')
        self.bddownload = ''
        if (len(download_selector) > 0):
            downloadlink = download_selector[0]
        else:
            download_selector = selector.xpath('//a[1]')
            for s in download_selector:
                if (len(s.xpath('./text()')) > 0) and ('百度' in s.xpath('./text()')[0]):
                    # //*[@id="content"]/p[11]/span/a[1]
                    try:
                        self.bddownload = (s.xpath('./@href')[0])
                        bdmmstr = (s.xpath('../text()[2]')[0])
                        bdmm = (re.search('：[ a-z0-9]*', bdmmstr))
                        if bdmm:
                            self.mm = ((bdmm.group()).split('：')[1])
                        return
                    except:
                        self.mm = ' '

            return
        
        htmlMebook = requests.get(downloadlink)
        selector = etree.HTML(htmlMebook.text)
        
        bdmmstr = (selector.xpath('/html/body/div[3]/p[6]/text()')[0])
        bdmm = (re.search('百度网盘密码：[ a-z0-9]*', bdmmstr))
        if bdmm:
            self.mm = ((bdmm.group()).split('：')[1])
            pans = selector.xpath('/html/body/div[5]/a')
            for pan in pans:
                if '百度' in str(pan.xpath('./text()')):
                    self.bddownload = (pan.xpath('./@href')[0])
                    # print(bddownload)
                    # return mm, bddownload

class BookInfo: # from mebook web to info
    def __init__(self, xpath):
        # //*[@id="primary"]/ul/li[9]/div[2]/h2/a
        # //*[@id="primary"]/ul/li[9]/div[2]/div/text()
        self.nameOrigin = xpath.xpath('./div[2]/h2/a/@title')[0]
        self.booklink = xpath.xpath('./div[2]/h2/a/@href')[0]
        self.downloadInfo = BookDownloadInfo(self.booklink)
        if(self.isBook()):
            self.bookName = self.BookName()
            self.zz = self.Zz()
            self.gxrq = xpath.xpath('./div[2]/div/text()')[0].split()[0]
    def isBook(self):
        return ('《' in self.nameOrigin)
    def BookName(self):
        return self.nameOrigin[self.nameOrigin.find('《')+1:self.nameOrigin.find('》')]
    def Zz(self): # authour
        return self.nameOrigin[self.nameOrigin.find('》')+1:self.nameOrigin.find('（', self.nameOrigin.find('》'))]
           
class BookInDB:
    def __init__(self, id):
        self.book = Book.objects.filter(id = id)
        self.downloadInfo = BookDownloadInfo(self.book[0].cclink)
    def zzSuccess(self):
        self.book.update(zzFlag = True, zzDate = datetime.date.today())
    def zzFail(self):
        self.book.update(zzFlag = True, bz = '百度盘无（和谐）' + self.book[0].bz)

class BooksFromDB: 
    def __init__(self, books):
        # boos is like Book.objects.filter(...) or all
        self.books = books
        self.loginFlag = False
    
    def login(self, browser):
        if not self.loginFlag:
            self.mypan = bdpan.BaiduPan(browser)
            self.mypan.login()
            self.loginFlag = True
        
    def zzBook(self):
        browser = webdriver.Firefox()
        
        for book in self.books:
            bookInDB = BookInDB(book.id)
            if (len(bookInDB.downloadInfo.bddownload) > 0):
                self.login(browser)
                if(self.mypan.zz(bookInDB.downloadInfo.bddownload, bookInDB.downloadInfo.mm)):
                    bookInDB.zzSuccess()
                else:
                    bookInDB.zzFail()
            

def mebook(startPage, endPage):
    for i in range(startPage, endPage+1):
        url  = 'http://mebook.cc/page/' + str(i)
        html = requests.get(url)
        selector = etree.HTML(html.text)
        endText = selector.xpath('//*[@id="container"]/div/h2/text()')
        if len(endText) > 0 and '传说' in endText[0]:
            print('mebook done')
            return  # 结束
        lis = selector.xpath('//*[@id="primary"]/ul/li')
        zz_page = True
        for li in lis:
            theBook = BookInfo(li)
            if (theBook.isBook()):
                bs = Book.objects.filter(bookname = theBook.bookName, zz = theBook.zz, gxsj = theBook.gxrq)
                if (len(bs)>0):
                    continue
                zz_page = False
                db = DoubanBook(theBook.bookName, theBook.zz)
                [tags, rating, bookUrl, summary] = (db.getBookInfo())
                #print(theBook.bookName, theBook.zz, tags, rating, bookUrl, summary)
                try:
                    rating = float(rating)
                except:
                    rating = 0
                bb = Book(bookname = theBook.bookName, zz=theBook.zz, gxsj = theBook.gxrq\
                        , tags=','.join(tags), rating=rating, cclink=theBook.booklink\
                        , dblink=bookUrl, bz=summary, zzFlag=0)
                bb.save()
                #print(theBook.bookName + ' ' + theBook.zz + ' ' + theBook.gxrq)
        print('the %d page done' % i)
        if (zz_page):
            return
        
'''
def downloadMebook(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    downloadlink = selector.xpath('//*[@id="content"]/div/p[6]/strong/a/@href')[0]
    
    htmlMebook = requests.get(downloadlink)
    selector = etree.HTML(htmlMebook.text)
    
    bdmmstr = (selector.xpath('/html/body/div[3]/p[6]/text()')[0])
    bdmm = (re.search('百度网盘密码：[a-z0-9]*', bdmmstr))
    if bdmm:
        mm = ((bdmm.group()).split('：')[1])
        pans = selector.xpath('/html/body/div[5]/a')
        for pan in pans:
            if '百度' in str(pan.xpath('./text()')):
                bddownload = (pan.xpath('./@href')[0])
                print(bddownload)
                return mm, bddownload
'''