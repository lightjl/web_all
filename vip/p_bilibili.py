from selenium import webdriver
import time
from vip.models import Moive_bilibili
from douban.doubanMoive import DoubanMoive

browser = webdriver.Firefox()

def get_moive_name(title):
    # 外国小哥欠了债，被迫接受实验，竟因祸得福有了闪电侠的超能力！片片解说《疯人院》
    name = ''
    try:
        name = title.split('《')[1].split('》')[0]
    except:
        name = title
    return name

def get_page(page, browser):
    url = 'https://space.bilibili.com/10119428/#/video?tid=0&page=%d&keyword=&order=pubdate' % page
    zz = '片片'
    browser.get(url)
    time.sleep(4)
    lis = browser.find_elements_by_xpath('//*[@id="submit-video-list"]/ul[2]/li')
    for li in lis:
        title = li.find_element_by_xpath('./a[2]').get_attribute('title')
        name = get_moive_name(title)
        href = li.find_element_by_xpath('./a[2]').get_attribute('href')
        mvs = Moive_bilibili.objects.filter(title=title, zz = zz)
        if (len(mvs) > 0):
            continue
        
        if name == title:
            moive_id = 0
        else:
            moive_db = DoubanMoive(name)
            moive_id = moive_db.moive_id
        mv = Moive_bilibili(moive_name=name, zz = zz, title = title, url=href, moive_id=moive_id)
        mv.save()
        
for i in range(4,16):
    get_page(i, browser)
