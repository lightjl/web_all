from selenium import webdriver
import time


web_Flag = True
if web_Flag:
    from vip.models import Moive_vip
    from douban.doubanMoive import DoubanMoive

url  = 'https://film.qq.com/film_all_list/allfilm.html?iarea=1'
bz = 'vip_qq'

# url = input('url:https://mebook.suning.com/ebookzhuanti.html?id=r-home-jx-topic1&title=SUPER%E4%B8%93%E4%BA%AB5000')
# bz = input('bz:super免费')

browser = webdriver.Firefox()
browser.get(url)

def check_page(lis):
    for li in lis[:]:
        name = li.find_element_by_xpath('./a').get_attribute('title')
        if web_Flag:
            ms = Moive_vip.objects.filter(name = name)
            if (len(ms)>0):
                continue
        # //*[@id="film_list"]/ul/li[2]/a
        url = li.find_element_by_xpath('./a').get_attribute('href')
        price = 0
        try:
            price_title = li.find_element_by_xpath('./a/i/img').get_attribute('alt')
        except:
            price_title = ''
        if price_title == '付费':
            price = 1
        if web_Flag:
            moive_db = DoubanMoive(name)
            mv = Moive_vip(name=name, url=url, bz=bz, price=price, moive_id=moive_db.moive_id)
            mv.save()
            
for i in range(91):
    lis = browser.find_elements_by_xpath('//*[@id="film_list"]/ul/li')
    check_page(lis)
    # next page
    browser.find_element_by_xpath('//*[@id="film_pager_small"]/a[2]/i').click()
    time.sleep(4)