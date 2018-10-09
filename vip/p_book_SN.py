from selenium import webdriver
import time
import pandas as pd
import numpy as np
from vip.models import Book_SN
from douban.doubanBook import DoubanBook

url  = 'https://mebook.suning.com/ebookzhuanti.html?id=r-home-jx-topic1&title=SUPER%E4%B8%93%E4%BA%AB5000'
bz = 'super免费'

# url = input('url:https://mebook.suning.com/ebookzhuanti.html?id=r-home-jx-topic1&title=SUPER%E4%B8%93%E4%BA%AB5000')
# bz = input('bz:super免费')

gundong = int(input('滚动多少:'))
browser = webdriver.Firefox()
browser.get(url)
while (gundong) > 0:
    for i in range(gundong):
        js="var q=document.documentElement.scrollTop=100000000"  
        browser.execute_script(js)  
        time.sleep(1)  
    gundong = int(input('滚动多少:'))
        
# 0元购
books = browser.find_elements_by_xpath('/html/body/div[2]/div/ul/li/a[*]')

for b in books[:]:
    name = b.find_element_by_xpath('./div/div[1]').text
    zz = b.find_element_by_xpath('./div/div[2]').text
    url = b.find_element_by_xpath('.').get_attribute('href')
    
    bs = Book_SN.objects.filter(name = name, zz = zz)
    if (len(bs)>0):
        continue
    book_DB = DoubanBook(name,zz)
    
    bs = Book_SN(name = name, zz = zz, url = url, bz = bz, book_id = book_DB.book_id)
    bs.save()