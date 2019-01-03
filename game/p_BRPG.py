from lxml import etree
import requests

from game.models import BRPG

def get_real_taobao(url):
    from urllib.parse import unquote
    if 'click' not in url:
        return (url)
    _refer = requests.get(url).url
    headers = {'Referer': _refer}
    url_unquote = unquote(_refer.split('tu=')[1], 'utf-8')
    print(url_unquote)
    return requests.get(url_unquote, headers=headers).url.split('&ali_trackid=')[0]

def price_maybe(price_str):
    price_list = price_str.replace(' ', '').split('-')
    if len(price_list) > 1:
        price_min = price_list[0]
        price_max = price_list[-1]
        if float(price_max) > 100 and float(price_max) > 2* float(price_min):
            price = price_max
        else:
            price = price_min
    else:
        price = price_list[0]
    return price

def check_page(page):
    url  = 'http://www.yihubg.com/find?gameWeight=1&page=' + str(page)
    # url  = 'http://www.yihubg.com/top?&page=' + str(page)
    html = requests.get(url)
    selector = etree.HTML(html.text)
    herf_base = 'http://www.yihubg.com'
    trs = selector.xpath('/html/body/div[2]/table/tbody/tr')
    for tr in trs:
        name = (tr.xpath('./td[2]/a/text()')[0])        
        name_eng = (tr.xpath('./td[2]/a/span/text()')[0])
        peoples = (tr.xpath('./td[3]/text()')[0].replace(' ', ''))
        mins = (tr.xpath('./td[4]/text()')[0].replace(' ', ''))
        hard = (tr.xpath('./td[5]/text()')[0])
        hard_level = (tr.xpath('./td[5]/span/text()')[0][1:-1])
        rating = (tr.xpath('./td[6]/text()')[0])
        
        games = BRPG.objects.filter(name_eng = name_eng)
        if (len(games)>0):
            continue
        
        href_tail = (tr.xpath('./td[2]/a/@href')[0])
        href_game = herf_base + href_tail
        html_game = requests.get(href_game)
        selector_game = etree.HTML(html_game.text)
        # age /html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/p[7]/span
        # year /html/body/div[2]/div[1]/div/div/div/div[3]/div[1]/text()
        # language /html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/div/p[2]
        age = (selector_game.xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/p[7]/span/text()')[0][:-1])
        publish_year = (selector_game.xpath('/html/body/div[2]/div[1]/div/div/div/div[3]/div[1]/text()')[0].replace(' ', '')[6:10])
        language = (selector_game.xpath('/html/body/div[2]/div[1]/div/div/div/div[2]/div[2]/div/p[2]/text()')[0].replace(' ', ''))
        tag = (selector_game.xpath('/html/body/div[2]/div[1]/div/div/div/div[3]/div[2]/div[4]/p[2]')[0].xpath('string(.)').replace(' ', '').replace('\n',''))
        tag += (selector_game.xpath('/html/body/div[2]/div[1]/div/div/div/div[3]/div[2]/div[5]/p[2]')[0].xpath('string(.)').replace(' ', '').replace('\n',''))
        #print(tr.xpath('./td[7]/text()'))
        
        if(len(tr.xpath('./td[7]/text()')) > 0 and tr.xpath('./td[7]/text()')[0] == '暂缺'):
            tb = False
            url_tb = ''
            price = 0
        else:
            tb = True
            
            url_tb = get_real_taobao(tr.xpath('./td[7]/a/@href')[0])
            html_tb = requests.get(url_tb, timeout=30)
            selector_tb = etree.HTML(html_tb.text)
            try:
                price_str = selector_tb.xpath('//*[@id="J_StrPrice"]/em[2]/text()')[0]
                price = price_maybe(price_str)
            except:
                price = 0
                   
               
           
        print('%s %s %s %s %s %s %s %s %r' % (name, name_eng, href_game, peoples, mins, hard, hard_level, rating, tb))
        print('%s %s %s %s' % (age, publish_year, language, tag))
        
        new_game = BRPG(name=name, name_eng=name_eng, href_game=href_game, peoples=peoples,\
                        mins=mins, hard=hard, hard_level=hard_level, rating=rating, tb=tb,\
                        age=age, publish_year=publish_year, language=language, tag=tag, \
                        url_tb=url_tb, price=price)
        new_game.save()