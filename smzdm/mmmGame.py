from lxml import etree
import requests
import json
import re
import time
from smzdm.models import mmmGame
import threading
from common.sendMail import sendMail
import datetime 

class Game:
    def __init__(self, id):
        self.game = mmmGame.objects.filter(id = id)
        self.game_price()
        self.notice()
        self.game.update(name = self.name, lowerPrice = self.lowerPrice, lowerDate = self.lowerDate
                         , currentPrice = self.currentPrice)
        # lowerPrice = self.lowerPrice,
        

    def game_price(self):
        html = requests.get(self.game[0].url)
        priceJson = json.loads(html.text)
        self.lowerPrice = priceJson['lowerPrice']
        if (len(priceJson['spName']) > 4):
            self.name = priceJson['spName']
        else:
            self.name = self.game[0].name
        self.currentPrice = priceJson['currentPrice']
        date = (re.search('\(.*\)', priceJson['lowerDate']))
        if date:
            dateStr = (date.group())[:-1].split('+')[0][1:]
            print(dateStr)
            self.lowerDate = time.strftime('%F', time.localtime(float(dateStr)/1000))
            
    def notice(self):
        if (self.game[0].currentPrice != self.currentPrice):
            self.game.update(currentDate = datetime.date.today())
        if (self.lowerPrice == self.currentPrice) \
            and (type(self.game[0].currentPrice) == type(None) or (self.game[0].currentPrice > self.currentPrice)):
            sendHotmail = threading.Thread(target=sendMail.sendMail, args=('buy: ' + self.name + ' ' + str(self.currentPrice), \
                'game: ' + self.game[0].tbUrl, 'ming188199@hotmail.com', 'hotmail', False))
            sendHotmail.start()
        if (self.currentPrice >= self.game[0].buyPrice + self.game[0].yj + self.game[0].cb):
            sendHotmail = threading.Thread(target=sendMail.sendMail, args=('sell: ' + self.name + ' ' + str(self.currentPrice), \
                'game: ' + self.game[0].tbUrl, 'ming188199@hotmail.com', 'hotmail', False))
            sendHotmail.start()
            