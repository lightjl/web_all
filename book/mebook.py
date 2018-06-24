from lxml import etree
import requests
from book.models import Book
from .doubanBook import DoubanBook

class BookInfo:
    def __init__(self, xpath):
        # //*[@id="primary"]/ul/li[9]/div[2]/h2/a
        # //*[@id="primary"]/ul/li[9]/div[2]/div/text()
        self.nameOrigin = xpath.xpath('./div[2]/h2/a/@title')[0]
        self.booklink = xpath.xpath('./div[2]/h2/a/@href')[0]
        if(self.isBook()):
            self.bookName = self.BookName()
            self.zz = self.Zz()
            self.gxrq = xpath.xpath('./div[2]/div/text()')[0].split()[0]
    def isBook(self):
        return ('《' in self.nameOrigin)
    def BookName(self):
        return self.nameOrigin[self.nameOrigin.find('《')+1:self.nameOrigin.find('》')]
    def Zz(self):
        return self.nameOrigin[self.nameOrigin.find('》')+1:self.nameOrigin.find('（', self.nameOrigin.find('》'))]
        

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
        for li in lis:
            theBook = BookInfo(li)
            if (theBook.isBook()):
                bs = Book.objects.filter(bookname = theBook.bookName, zz = theBook.zz, gxsj = theBook.gxrq)
                if (len(bs)>0):
                    continue
                db = DoubanBook(theBook.bookName, theBook.zz)
                [tags, rating, bookUrl, summary] = (db.getBookInfo())
                #print(theBook.bookName, theBook.zz, tags, rating, bookUrl, summary)
                try:
                    rating = float(rating)
                except:
                    rating = 0
                bb = Book(bookname = theBook.bookName, zz=theBook.zz, gxsj = theBook.gxrq\
                        , tags=','.join(tags), rating=rating, cclink=theBook.booklink\
                        , dblink=bookUrl, bz=summary)
                bb.save()
                #print(theBook.bookName + ' ' + theBook.zz + ' ' + theBook.gxrq)
        print('the %d page done' % i)
        