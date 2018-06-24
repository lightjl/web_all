import requests
import json
import time
from common.proxy import proxy
import logging

class DoubanBook:
    def __init__(self, name, author=None):
        self.useProxy = False
        self.name = name
        self.author = author
        #self.checkUrl = 'http://www.cbip.cn/Query.aspx?search_str0=' + urllib.request.quote(name)
        self.checkUrl = 'https://api.douban.com/v2/book/search?q=' + name
        if author is not None:
            self.checkUrl += "+"+author
            
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
        try:
            html = requests.get(self.checkUrl, proxies=self.proxyDict)
            booksJson = json.loads(html.content.decode())
        except:
            return ['' for i in range(4)]
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
        self.tags = [tag['title'] for tag in (booksJson['books'][0]['tags'])]
        #print(tags)
        self.bookUrl = booksJson['books'][0]['alt']
        #print(self.bookUrl)
        self.summary = booksJson['books'][0]['summary']
        #print(self.summary)
        self.rating = booksJson['books'][0]['rating']['average']
        return [self.tags, self.rating, self.bookUrl, self.summary]

'''
yb = DoubanBook('从无穷开始：科学的困惑与疆界', '让•皮埃尔•卢米涅 等')
[tags, rating, bookUrl, summary] = (yb.getBookInfo())
'''