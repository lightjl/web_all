from lxml import etree
import requests
import time
import json
import datetime

web_Flag = True
if web_Flag:
    from douban.models import Moive

class DoubanMoive:
    def __init__(self, name):
        self.name = name
        #self.checkUrl = 'http://www.cbip.cn/Query.aspx?search_str0=' + urllib.request.quote(name)
        self.checkUrl = 'http://api.douban.com/v2/movie/search?q=' + name + '&count=1'
        self.moive_id = 0
        self.getInfo()

    def getInfo(self):
        if web_Flag:
            ms = Moive.objects.filter(name = self.name)
            if (len(ms) > 0): # todo 半年更新
                the_moive = ms[0]
                self.tags = the_moive.tags
                self.rating = the_moive.rating
                self.year = the_moive.year
                self.moive_id = the_moive.id
                return [self.name, self.year, self.tags, self.rating]
        try:
            html = requests.get(self.checkUrl)
            booksJson = json.loads(html.content.decode())
        except:
            return ['' for i in range(4)]
        
        while ('code' in booksJson or len(booksJson['subjects']) == 0):
            try:
                time.sleep(5*60)
                html = requests.get(self.checkUrl)
                booksJson = json.loads(html.content.decode())
            except:
                return ['' for i in range(4)]
        #print(booksJson)

#         if len(booksJson['books']) == 0:
#             return ['' for i in range(2)]
#         print(booksJson['subjects'])
        self.tags = ','.join(tag for tag in (booksJson['subjects'][0]['genres']))
        #print(tags)
        #print(self.bookUrl)
        #print(self.summary)
        self.rating = booksJson['subjects'][0]['rating']['average']
        self.year = booksJson['subjects'][0]['year']
        if web_Flag:
            moive = Moive(name = self.name, zz = '', tags = self.tags,  year = self.year,  gxsj = datetime.datetime.now(),
                          rating = self.rating, link = '',    bz = '')
            moive.save()
            self.moive_id = Moive.objects.filter(name = self.name)[0].id
        return [self.name, self.year, self.tags, self.rating]
