import account
from selenium import webdriver
import re
import time
from qieman.models import Fund
import datetime
from django.db.models import Min
from lxml import etree
import requests
from common.sendMail import sendMail
import threading

class qieman_login:
    def __init__(self):
        self.browser = webdriver.Firefox()
        url = 'https://qieman.com/user/login'
        self.browser.get(url)
        self.login()
        
    def login(self):
        browser = self.browser
        browser.find_element_by_xpath('//*[@id="phone"]').send_keys(account.qieman_phone)
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(account.qieman_password)
        browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/div/div/span/button').click()
        
class fund_qieman:
    def __init__(self, tr, browser, zlr='Ebig'):
        self.tr = tr
        self.zlr = zlr
        self.browser = browser # 专门用来采集基金购入数据
        self.code() # 此处区分是谁的仓位
#         print(self.code)
        self.copies()
        self.name()
        self.yk()
        

    def code(self):
        code_str = (re.search('\([.0-9]+\)', self.tr.text))
        if code_str:
            self.code = (code_str.group()[1:-1])
            if self.zlr == 'Ebig':
                self.url = 'https://qieman.com/longwin/funds/%s?investType=E' % self.code
            else:
                self.url = 'https://qieman.com/longwin/position/%s' % self.code
            return self.code
    
    def copies(self):
        copies_str = (re.search('有[.0-9]+份', self.tr.find_element_by_xpath('../../td[2]/div[1]').text))
        if copies_str:
            self.copies = (copies_str.group()[1:-1])
            return self.copies
    
    def name(self):
#         self.name = self.tr.text.split('(')[0] # 全称
        self.name = self.tr.find_element_by_xpath('..//div[1]').text
        return self.name
    
    def yk(self):
        self.yk = self.tr.find_element_by_xpath('../../td[2]/div[2]/span').text
        return self.yk
        
    def mx(self):
        # todo 处理买卖数据
        browser = self.browser
        browser.get(self.url)
        trs = browser.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/section[4]/table/tbody/tr')
        try:
            min_price = float(trs[0].find_element_by_xpath('./td[1]/div[2]/span').text)
        except:
            min_price = 99
        for tr in trs[1:]:
            tmp = float(tr.find_element_by_xpath('./td[1]/div[2]/span').text)
            if (tmp <= min_price):
                min_price = tmp
        try:
            price_hold = float(browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/section[2]/div/div[2]/div/span[2]/span').text)
        except:
            price_hold = min_price
        if (min_price > price_hold):
            min_price = price_hold
        self.jz = float(browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/section[2]/div/div[4]/div/span[2]/span').text)
        self.price_min = min_price
        self.price_hold = price_hold
        

class fund_qieman_me:
    def __init__(self, tr, browser):
        self.tr = tr
        self.browser = browser # 专门用来采集基金购入数据
        self.copies()
        self.name()
        self.code() # 此处区分是谁的仓位
        self.yk()

    def code(self):
        fs = Fund.objects.filter(name=self.name)
        self.code = fs[0].code
        self.url = 'https://qieman.com/longwin/position/%s' % self.code
        return self.code
    
    def copies(self):
        self.copies = float(self.tr.find_element_by_xpath('./td[1]/div[2]/span[1]').text[:-1])
        # //*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/div[7]/section[1]/div/table/tbody/tr[1]/td[1]/div[2]/span[1]
        # //*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/div[7]/section[1]/div/table/tbody/tr[1]/td[1]/div[2]/span[1]/text()[1]
        return self.copies

    def name(self):
        self.name = self.tr.find_element_by_xpath('./td[1]/div[1]').text
#         //*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/div[7]/section[1]/div/table/tbody/tr[1]/td[1]/div[1]
        return self.name
    
    def yk(self):
        self.yk = self.tr.find_element_by_xpath('./td[2]/div[3]/span[2]').text
        # //*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/div[7]/section[1]/div/table/tbody/tr[1]/td[2]/div[3]/span[2]/text()
        return self.yk
        
    def mx(self):
        # todo 处理买卖数据
        browser = self.browser
        self.browser.get(self.url)
        time.sleep(4)
        self.trs = self.browser.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/div[3]/table/tbody/tr')

        #price_test = float(trs_test[0].find_element_by_xpath('./td[1]/div[2]/span/span').text)
        #print(price_test)

        try:
            min_price = float(self.trs[0].find_element_by_xpath('./td[1]/div[2]/span/span').text)
        except:
            min_price = 99
        for tr in self.trs[1:]:
            try:
                tmp = float(tr.find_element_by_xpath('./td[1]/div[2]/span/span').text)
                if (tmp <= min_price):
                    min_price = tmp
            except:
                continue
        try:
            price_hold = float(self.browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div/div[4]/div/span[2]/span').text)
        except:
            price_hold = min_price
        if (min_price > price_hold):
            min_price = price_hold
        self.price_min = min_price
        self.price_hold = price_hold
        
class longwin_detail:
    def __init__(self):
        today = datetime.date.today()
        today_11 = datetime.datetime(today.year, today.month, today.day, 11)
        while True:
            min_gxsj = Fund.objects.all().aggregate(Min('gxsj'))['gxsj__min']
            if min_gxsj < today_11:
                self.check()
            else:
                break
        
    def check(self):
        browser = webdriver.Firefox()
        url = 'https://qieman.com/longwin/detail'
        browser.get(url)
        trs = browser.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/table[2]/tbody/tr[*]/td[1]/div[2]')
        # //*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/table[2]/tbody/tr[2]/td[1]/div[1]
        # //*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/table[2]/tbody/tr[*]/td[1]/div[2]
        browser_fund = webdriver.Firefox()
        today = datetime.date.today()
        today_11 = datetime.datetime(today.year, today.month, today.day, 11)
        for tr in trs:
            tmp = fund_qieman(tr, browser_fund)
            fs = Fund.objects.filter(code=tmp.code, name=tmp.name)
            if (len(fs)>0): #已有
                if fs[0].gxsj >= today_11:
                    continue
                else:
                    tmp.mx()
                    fs.update(code=tmp.code, name=tmp.name, fs=tmp.copies, yk=tmp.yk, price_min=tmp.price_min, price_hold=tmp.price_hold, jz=tmp.jz\
                              ,gxsj=today_11)
            else:
                tmp.mx()
                f = Fund(code=tmp.code, name=tmp.name, fs=tmp.copies, yk=tmp.yk, price_min=tmp.price_min, price_hold=tmp.price_hold, jz=tmp.jz\
                         ,gxsj=today_11)
                f.save()
            print(tmp.code, tmp.name, tmp.price_min, tmp.price_hold, tmp.yk, tmp.jz)
        browser.quit()
        browser_fund.quit()
        
class longwin_detail_my:
    def __init__(self):
        today = datetime.date.today()
        today_12 = datetime.datetime(today.year, today.month, today.day, 12)
        min_gxsj = Fund.objects.all().aggregate(Min('gxsj'))['gxsj__min']
        if min_gxsj < today_12:
            self.me = qieman_login()
            url = 'https://qieman.com/longwin/asset'
            self.me.browser.get(url)
            self.my_fund = qieman_login()
            while min_gxsj < today_12:
                self.check()
                min_gxsj = Fund.objects.all().aggregate(Min('gxsj'))['gxsj__min']
            self.quit()
    
    def check(self):
        self.trs = self.me.browser.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/div/div/div/div[7]/section[1]/div/table/tbody/tr')
    
        today = datetime.date.today()
        today_12 = datetime.datetime(today.year, today.month, today.day, 12)
        
        for tr in self.trs:
            tmp = fund_qieman_me(tr, self.my_fund.browser)
            fs = Fund.objects.filter(code=tmp.code, name=tmp.name)
            if(fs[0].gxsj >= today_12):
                continue
            tmp.mx()
            fs.update(fs_my=tmp.copies, yk_my=tmp.yk, price_min_my=tmp.price_min, price_hold_my=tmp.price_hold, gxsj=today_12)
            print(tmp.code, tmp.name, tmp.price_min, tmp.price_hold, tmp.yk)
            
    def quit(self):
        self.me.browser.quit()
        self.my_fund.browser.quit()
        
class Fund_deal:
    def __init__(self):
        self.fs = Fund.objects.all()
        today = datetime.date.today()
        self.today_14 = datetime.datetime(today.year, today.month, today.day, 14)
        self.today_15 = datetime.datetime(today.year, today.month, today.day, 15)
        
    def deal(self):
        if(datetime.datetime.now() < self.today_14):
            return
        for f in self.fs:
            if f.gxsj >= self.today_14:
                continue
            url = 'http://fund.eastmoney.com/%s.html?spm=search' % f.code
            html = requests.get(url)
            html.encoding = 'utf-8'
            selector = etree.HTML(html.text)
            try:
                gszzl = float(selector.xpath('//*[@id="gz_gszzl"]/text()')[0][:-1])
            except:
                gszzl = 0
            f.gxsj = self.today_14
            f.gszzl = gszzl
            f.save()
            
    def buy(self):
        if datetime.datetime.now() < self.today_14:
            reutrn
        min_gxsj = Fund.objects.all().aggregate(Min('gxsj'))['gxsj__min']
        if min_gxsj == self.today_15:
            return
        while True:
            min_gxsj = Fund.objects.all().aggregate(Min('gxsj'))['gxsj__min']
            if min_gxsj < self.today_14:
                self.deal()
            else:
                break
        texts = ''
        for f in self.fs:
            gz = f.jz * (1 + f.gszzl/100)
            if (f.price_min == 99):
                continue
            buy = 0
            try:
                fs_my = float(f.fs_my)
            except:
                fs_my = 0
            if f.price_min * 0.6 >= gz:
                buy = 2 * f.fs - fs_my
            elif f.price_min * 0.7 >= gz:
                buy = 1.6 * f.fs - fs_my
            elif f.price_min * 0.8 >= gz:
                buy = 1.3 * f.fs - fs_my
            elif f.price_min * 0.9 >= gz:
                buy = 1.1 * f.fs - fs_my
            elif f.price_min >= gz:
                buy = f.fs - fs_my
            f.gxsj = self.today_15
            f.save()
            
            if buy != 0:
                texts += ('%s %s buy=%.2f份 price_min=%.2f gz=%.2f fs=%.2f, fs_my=%.2f\n' % (f.code, f.name, buy, f.price_min, gz, f.fs, fs_my))
        
        print(texts)
        if (len(texts) > 0):
            sendMail.sendMail('qmjj: buy', texts, changeReceiver=True)