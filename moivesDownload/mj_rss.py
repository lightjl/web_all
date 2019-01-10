import sys
sys.path.append('..')
import requests
from bs4 import BeautifulSoup
import re
from moivesDownload import moiveE
from lxml import etree
import logging
import time
from multiprocessing import Process, Value
import threading
import os
import feedparser
from moivesDownload.models import Rss
from django.http import HttpResponse

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

def download_this_or_not(name):
    if ('mp4' in name) or ('MP4' in name):
        if  ('Chi_Eng' in name) or (('中' in name) and ('字幕' in name)):
            return True
    return False

def do_with_rss(rss_url):
    myMoives = moiveE.moives()
    d = feedparser.parse(rss_url)
    for i in d.entries:
        if download_this_or_not(i.title):
            mv = moiveE.moiveE(i.title, i.magnet)
            myMoives.send(mv)

def find_moives_from_rss(request):  # 
    rss = Rss.objects.all()
    for r in rss:
        do_with_rss(r.rss_url)
    return HttpResponse("well done")

