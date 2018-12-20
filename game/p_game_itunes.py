from lxml import etree
import requests

from game.models import game_itunes

def resons(selector):
    texts = []
    for i in range(5,8):
        texts = selector.xpath('//div[@id]/section[%d]/div/div[1]/dl/div[*]/dd/text()' % i)
        if len(texts) != 0:
            break
    result_text = ''
    for text in texts:
        if '/' in text:
            result_text += (text) + '\n'
    return result_text

def language_game(selector):
    texts = []
    for i in range(5,8):
        texts = selector.xpath('//div[@id]/section[%d]/div/div[1]/dl/div[*]/dd/span/span/span/text()' % i)
        if len(texts) != 0:
            break
#     print(texts)
    for text in texts:
        if ('文' in text or '语' in text):
            return text.replace(' ', '').replace('\n', '')
        
def str2num(string):
    if string.isdigit():
        return int(string)
    if 'M' in string:
        return float(string[:-1])*1e6
    if 'K' in string:
        return float(string[:-1])*1e3
    
def info_game(name, url_game, tag):
    html_game = requests.get(url_game)
    selector_game = etree.HTML(html_game.text)
    # age
    age = (selector_game.xpath('//div[@id]/section[1]/div/div[2]/header/h1/span/text()')[0][:-1])
    # 
    try:
        rating_str = selector_game.xpath('//figure[@id]/figcaption/text()')[0]
        rating = rating_str.split('，')[0]
        r_people = str2num(rating_str.split('，')[1].split()[0])
    except:
        rating = '0'
        r_people = 0
    # print(rating + 'people:' + str(r_people))
    content = (resons(selector_game))
    language = language_game(selector_game)
    if not language:
        language = 'None'
#     try:
#         print(selector_game.xpath('//div[@id]/section[6]/div/div[1]/dl/div[7]/dd/text()')[0])
#     except:
#         pass
    price = -1
    in_app_purchase = True
    for i in range(1,4):
        try:
            price_str = (selector_game.xpath('//div[@id]/section[1]/div/div[2]/header/ul/li[%d]/ul/li[1]/text()' % i))[0]
        except:
            continue
        if price_str[0] == '¥':
            price = float(price_str[1:].replace(',', ''))
        elif price_str[0] == '免':
            price = 0
        if price >= 0:
            try:
                tmp = (selector_game.xpath('//div[@id]/section[1]/div/div[2]/header/ul/li[%d]/ul/li[2]/text()' % i)[0])
                in_app_purchase = True
            except:
                in_app_purchase = False
    # print(str(price) + ' in_app_purchase: ' + str(in_app_purchase))
    gi = game_itunes(name = name, url = url_game, age = age, rating = rating, r_people = r_people\
                     , content = content, price = price, in_app_purchase = in_app_purchase, tag = tag, language = language)
    gi.save()
    
def game_index(url, tag):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    lis = selector.xpath('//*[@id="selectedcontent"]/div[1]/ul/li')
    for li in lis[:]:
        # //*[@id="selectedcontent"]/div[1]/ul/li[1]/a
        name = (li.xpath('./a/text()')[0])
        gs = game_itunes.objects.filter(name = name)
        if (len(gs)>0):
            continue
        url_game = (li.xpath('./a/@href')[0])
        # print(url_game)
        info_game(name, url_game, tag)