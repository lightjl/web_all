import requests
import json
import time
import logging
import datetime

web_Flag = True
if web_Flag:
    from common.proxy import proxy
    from douban.models import Book

class DoubanBook:
    def __init__(self, name, author=None):
        self.useProxy = False
        self.name = name
        self.author = author
        #self.checkUrl = 'http://www.cbip.cn/Query.aspx?search_str0=' + urllib.request.quote(name)
        self.checkUrl = 'https://api.douban.com/v2/book/search?q=' + name
        if author is not None:
            self.checkUrl += "+"+author
        if web_Flag:
            finder = proxy.XiciProxyFinder("http://www.xicidaili.com/wt/")
            self.ppool_instance = proxy.ProxyPool(finder)
            self.http_proxy = self.ppool_instance.get_one_proxy()
            self.proxyDict = { 
                  "http"  : self.http_proxy, 
                }
        #print(self.ppool_instance.get_one_proxy())
        #self.checkUrl = 'http://www.cbip.cn/Query.aspx?search_str0=green'
        # print(self.checkUrl)

    def getBookInfo(self):
        
        if web_Flag:
            if self.author is None:
                bs = Book.objects.filter(name = self.name)
            else:
                bs = Book.objects.filter(name = self.name, zz = self.author)
            if (len(bs)>0): # todo 半年更新
                the_book = bs[0]
                return [the_book.name, the_book.zz, the_book.tags, the_book.rating, the_book.link, the_book.zz]
        
        try:
            html = requests.get(self.checkUrl)
            booksJson = json.loads(html.content.decode())
        except:
            return ['' for i in range(6)]
        #print(booksJson)
        while ('code' in booksJson):
            if self.useProxy:
                self.ppool_instance.delpool(self.http_proxy)
                self.http_proxy = self.ppool_instance.get_one_proxy()
                self.proxyDict = {
                  "http"  : self.http_proxy, 
                  }
            try:
                if self.useProxy:
                    html = requests.get(self.checkUrl, proxies=self.proxyDict)
                else:
                    logging.critical('sleep 10min.')
                    time.sleep(5*60)
                    html = requests.get(self.checkUrl)
                booksJson = json.loads(html.content.decode())
            except:
                return ['' for i in range(4)]

        if len(booksJson['books']) == 0:
            return ['' for i in range(4)]
        self.tags = ','.join(tag['title'] for tag in (booksJson['books'][0]['tags']) )
        #print(tags)
        self.bookUrl = booksJson['books'][0]['alt']
        #print(self.bookUrl)
        self.summary = booksJson['books'][0]['summary']
        #print(self.summary)
        self.rating = booksJson['books'][0]['rating']['average']
        if self.author is None:
            self.author = ','.join(zz for zz in booksJson['books'][0]['author'] ) 
        if web_Flag:
            bs = Book(name = self.name
                      ,zz = self.author
                      ,tags = self.tags
                      ,gxsj = datetime.datetime.now()
                      ,rating = self.rating
                      ,link = self.bookUrl
                      ,bz = self.summary
                      )
            bs.save()
        return [self.name, self.author, self.tags, self.rating, self.bookUrl, self.summary]

'''
yb = DoubanBook('从无穷开始：科学的困惑与疆界', '让•皮埃尔•卢米涅 等')
[tags, rating, bookUrl, summary] = (yb.getBookInfo())

{"count":6,"start":0,"total":6,"books":[{"rating":{"max":10,"numRaters":12,"average":"7.4","min":0},
"subtitle":"科学的困惑与疆界","author":["[法] 让－皮埃尔·卢米涅","[法] 马克·拉雪茨－雷"],
pubdate":"2018-4","tags":[{"count":16,"name":"数学","title":"数学"},{"count":13,"name":"科普","title":"科普"},{"count":7,"name":"科学","title":"科学"},{"count":7,"name":"物理","title":"物理"},{"count":4,"name":"无穷","title":"无穷"},{"count":3,"name":"法国","title":"法国"},{"count":3,"name":"无限","title":"无限"},

'''