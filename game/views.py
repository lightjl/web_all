from django.shortcuts import render
from . import p_game, p_BRPG, p_game_itunes
from django.http import HttpResponse
import string
from lxml import etree
import requests
# Create your views here.

def Check_game(request):
    for page in range(0, 20):
        p_game.check_page(page)
    return HttpResponse('check game done')


def Check_BRPG(request):
    for page in range(1, 5):
        p_BRPG.check_page(page)
    return HttpResponse('check BRPG done')

def find_all_page(url, tag):
    html_page = requests.get(url)
    selector_page = etree.HTML(html_page.text)
    pages = selector_page.xpath('//div[@id]/ul[2]/li[*]/a/@href')
    for page in pages[1:-1]:
        p_game_itunes.game_index(page, tag)

def Check_game_itunes(request):
    url_list = [('https://itunes.apple.com/cn/genre/ios-%E6%B8%B8%E6%88%8F-%E7%AD%96%E7%95%A5%E6%B8%B8%E6%88%8F/id7017?mt=8', '策略'),
                ('https://itunes.apple.com/cn/genre/ios-%E6%B8%B8%E6%88%8F-%E7%9B%8A%E6%99%BA%E8%A7%A3%E8%B0%9C/id7012?mt=8', '益智'),
                ('https://itunes.apple.com/cn/genre/ios-%E6%B8%B8%E6%88%8F-%E5%86%92%E9%99%A9%E6%B8%B8%E6%88%8F/id7002?mt=8', '冒险'),
                ]
    for url in url_list[1:]:
    #         p_game_itunes.game_index(url[0], url[1])
        for i in (string.ascii_uppercase[:]):
            url_letter1 = (url[0] + '&letter=' + i) 
            p_game_itunes.game_index(url_letter1, url[1])
            find_all_page(url_letter1, url[1])
        url_letter1 = url[0] + '&letter=*'
        p_game_itunes.game_index(url_letter1, url[1])
        find_all_page(url_letter1, url[1])
    return HttpResponse('check game_itunes done')