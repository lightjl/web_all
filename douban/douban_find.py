from selenium import webdriver
import time
import requests
from lxml import etree
from douban.models import db_web
import json
import requests

class douban_web_find:
    def __init__(self):
        self.browser = webdriver.Chrome()
    
    def check_dm(self):
        # 动漫 7分以上
        browser = self.browser
        url = 'https://movie.douban.com/tag/?dt_dapp=1#/?sort=R&range=7,10&tags=动漫'
        browser.get(url)
        self.xs = '动漫'
        self.page_check()
        
    def check_ms(self, begin, ms):
        for m in ms[begin:]:
            # link //*[@id="app"]/div/div[1]/div[3]/a[1]
            # name //*[@id="app"]/div/div[1]/div[3]/a[1]/p/span[1]
            # rating //*[@id="app"]/div/div[1]/div[3]/a[1]/p/span[2]
            # id //*[@id="app"]/div/div[1]/div[3]/a[1]/div
            name_xpath = './p/span[1]'
            rating_xpath = './p/span[2]'
            id_xpath = './div'
    
            link = m.get_attribute('href')
            name = m.find_element_by_xpath(name_xpath).text
            rating = m.find_element_by_xpath(rating_xpath).text
            doubanID = m.find_element_by_xpath(id_xpath).get_attribute('data-id')
            # print(name, doubanID, link, rating)
            dbs = db_web.objects.filter(name = name, doubanID = doubanID, xs = self.xs)
            if (len(dbs)>0):
                continue
            dbs = db_web(name = name, doubanID = doubanID, link = link, rating = rating, xs = self.xs)
            dbs.save()
        
    def page_check(self):
        browser = self.browser
        moives_xpath = '//*[@id="app"]/div/div[1]/div[3]/a'
        more_xpath = '//a[@class="more"]'
        begin = 0
        while True:
            ms = browser.find_elements_by_xpath(moives_xpath)
            self.check_ms(begin, ms)
            begin = len(ms)
            try:
                browser.find_element_by_xpath(more_xpath).click()
                time.sleep(4)
            except:
                break
        
class douban_web_mx:
    def __init__(self, url):
        self.url = url
        
    def kbf_infos(self, selector):
        kbf_xpath = '//a[@class="playBtn"]'
        price_xpath = '../span/span'
        info = []
        for x in selector.xpath(kbf_xpath):
            wz = x.xpath('./text()')[0].strip()
            price = x.xpath(price_xpath + '/text()')[0].strip()
            info.append(wz + price)
        return ';'.join(info)
    
    def db_infos(self, selector):
        texts_xpath = '//*[@id="info"]'
        texts = selector.xpath(texts_xpath + '/text()')
        ith = 0
        info = []
        for text in texts:
            tmp = text.strip()
            if (len(tmp)>1 or tmp.isdigit()):
                ith += 1
                if (tmp.isdigit()):
                    tmp += '集'
                info.append(tmp)
                
        return ';'.join(info)
        
    def douban_infos_all(self):
        html = requests.get(self.url)
        selector = etree.HTML(html.text)
        doubanID = self.url.split('/')[-2]
    
        tags_xpath = '//*[@id="info"]/span[@property="v:genre"]'
        IMDBid_xpath = '//*[@id="info"]/a[starts-with(text(), "tt")]'
        bz_xpath = '//span[@property="v:summary"]'
        rating_xpath = '//*[@id="interest_sectl"]/div/div[2]/strong'
    
        infos = self.db_infos(selector)
        tags = ';'.join(selector.xpath(tags_xpath + '/text()'))
        rating = selector.xpath(rating_xpath + '/text()')[0]
        try:
            IMDBid = selector.xpath(IMDBid_xpath + '/text()')[0]
        except:
            IMDBid = ''
        bz = selector.xpath(bz_xpath + '/text()')
        bz = ' '.join(list(map(lambda x: x.strip(), bz)))
        kbf = self.kbf_infos(selector)
        return (doubanID, infos, tags, IMDBid, kbf, bz, rating)
    
class imdb_info():
    def __init__(self, name = '', id = '', year = 0):
        #if movie name contains any value from the replace[] list, replace it with space 
        self.apikey = "&apikey=9b925aaa"
        self.name = name
        self.id = id
        self.year = year
        self.imdb_url()
    
    def imdb_url(self):
        apikey = self.apikey
        name = self.name
        id = self.id
        year = self.year
        name = name.strip()
        #"apikey=9b925aaa" is set for now, you can create the key from http://www.omdbapi.com/apikey.aspx and change it
        if len(id) > 0:
            url = "http://www.omdbapi.com/?i="+id
        else:
            url = "http://www.omdbapi.com/?t="+name
        if year != 0:
            url += "&y="+str(year)
        url += apikey    
        self.url = url
    
    def imdb_infos(self):
        url = self.url
        html = requests.get(url)
        try:
            imdbJson = json.loads(html.content.decode())
        except:
            print(self.id)
            return
        
        Response = imdbJson['Response']
        if(Response == 'False'):
            return
        Title = imdbJson['Title']
        Year = imdbJson['Year']
        Rated = imdbJson['Rated']
        Released = imdbJson['Released']
        Runtime = imdbJson['Runtime']
        Genre = imdbJson['Genre']
        Director = imdbJson['Director']
        Writer = imdbJson['Writer']
        Actors = imdbJson['Actors']
        Plot = imdbJson['Plot']
        Language = imdbJson['Language']
        Country = imdbJson['Country']
        Awards = imdbJson['Awards']
        Poster = imdbJson['Poster']
        Ratings = imdbJson['Ratings']
        Metascore = imdbJson['Metascore']
        imdbRating = imdbJson['imdbRating']
        imdbVotes = imdbJson['imdbVotes']
        imdbID = imdbJson['imdbID']
        Type = imdbJson['Type']
        try:
            totalSeasons = imdbJson['totalSeasons']
        except:
            totalSeasons = '0'
        return (Title, Year, Rated, Released, Runtime, Genre, Director, Writer, \
                Actors, Plot, Language, Country, Awards, Poster, Metascore, \
                imdbRating, imdbVotes, imdbID, Type, totalSeasons)