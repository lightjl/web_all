from lxml import etree
import requests
import json
import re
from game.models import game
from datetime import datetime

def remove_char(str_remove):
    list_char = '：-:\' '
    for char in list_char:
        str_remove = str_remove.replace(char, '')
    return str_remove

def find_name_eng(other_name):
    for str_name in other_name.split(','):
        if(remove_char(str_name).encode('UTF-8').isalnum()):
            return str_name

def decode_esrb(png):
    if png == 'EC':
        return 3
    elif png == 'E':
        return 6
    elif png == 'E10plus':
        return 10
    elif png == 'T':
        return 13
    elif png == 'M':
        return 17
    elif png == 'AO':
        return 18

def check_page(page):
    url = 'http://www.ign.com/reviews/games?startIndex=' + str(page*25)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)

    divs = selector.xpath('//*[@id="item-list"]/div[2]/div')
    for div in divs:
        name_eng = (div.xpath('./div[2]/div[1]/h3/a/text()')[0].strip())
        rating = float(div.xpath('./div[4]/div/a/span[1]/text()')[0])
        date_str = div.xpath('./div[3]/div/text()')[0]
        review_date = datetime.strptime(date_str,'%B %d, %Y').strftime('%Y-%m-%d')

        # ./div[3]/div
        games = game.objects.filter(name_eng = name_eng)
        if (len(games)>0):
            continue
#     ign 中国
#     url = 'http://www.ign.xn--fiqs8s/article/review?page=' + str(page)
#     html = requests.get(url)
#     selector = etree.HTML(html.text)
#     lis = selector.xpath('//*[@id="content"]/ul[1]/li')
#     for li in lis:
#         thing_type = li.xpath('./article/div[2]/b/text()')[0]
#         if thing_type != 'Videogame':
#             continue
#         name = (li.xpath('./article/div[2]/h2/a/text()')[0])
# #         print(name)
#         try:
#             rating = float((li.xpath('./article/div[4]/div/span/text()')[0]))
#         except:
#             continue

        urlvgame = 'http://www.vgtime.com/search/load.jhtml?keyword=' + name_eng + '&type=game&page=1&pageSize=12'
        htmlvgame = requests.get(urlvgame)
        print(urlvgame)
        try:
            json_game = json.loads(htmlvgame.text)
        except:
            continue
        try:
            tag = json.loads(json_game['data'][0]['content'])['gameTag']
        except:
            continue
        platform = json.loads(json_game['data'][0]['content'])['platform']
        name = json.loads(json_game['data'][0]['content'])['name']
        print(name_eng + ' ' + name)
        if(not (name_eng)):
            continue
#         print(name_eng)
        numbers_str = (re.search('\d+', name_eng))
        if numbers_str:
            #print((numbers_str.group()))
            series = int((numbers_str.group()))
        else:
            series = 0
        url_esrb = 'http://www.esrb.org/ratings/search.aspx?from=home&titleOrPublisher=' + name_eng
        html_esrb =  requests.get(url_esrb)
        selector_esrb = etree.HTML(html_esrb.text)
        try:
            png = selector_esrb.xpath('//tbody[@data-title]/tr[1]/td[3]/img/@src')[0].split('/')[-1][:-4]
            esrb = decode_esrb(png)
            content_descriptors = ' '.join(selector_esrb.xpath('//tbody[@data-title]/tr[1]/td[4]/text()')[0].split())
        except:
            esrb = 3
            content_descriptors = '无esrb'
        
        
        print('%s %s %f %s %s %d %d %s' % (name, name_eng, rating, tag, platform, series, esrb, content_descriptors))
    # 
        new_game = game(name=name, name_eng=name_eng, rating=rating, review_date=review_date,\
                        tag=tag, platform=platform, series=series, esrb=esrb, content_descriptors=content_descriptors)
        new_game.save()
    # 