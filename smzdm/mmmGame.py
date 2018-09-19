from lxml import etree
import requests
import json
import re
import time
from smzdm.models import mmmGame
import threading
from common.sendMail import sendMail
import datetime 
from email_os import p_email_os

class Game:
    def __init__(self, id):
        self.email = p_email_os.Email_os()
        self.game = mmmGame.objects.filter(id = id)
        if(self.game_price()):
            self.notice()
            self.game.update(ce = self.currentPrice - self.lowerPrice
                             , lowerPrice = self.lowerPrice, lowerDate = self.lowerDate
                             , currentPrice = self.currentPrice)

        # lowerPrice = self.lowerPrice,
        

    def game_price(self):
        try:
            html = requests.get(self.game[0].url)
            priceJson = json.loads(html.text)
            self.lowerPrice = priceJson['lowerPrice']
            # print(priceJson['spName'])
            self.currentPrice = priceJson['currentPrice']
            if (len(priceJson['spName']) > 4):
                self.name = priceJson['spName']
            elif self.currentPrice == 0:
               return False
            # print(self.currentPrice)
            date = (re.search('\(.*\)', priceJson['lowerDate']))
            if date:
                dateStr = (date.group())[:-1].split('+')[0][1:]
                # print(dateStr)
                self.lowerDate = time.strftime('%F', time.localtime(float(dateStr)/1000))
            return True
        except:
            return False
            
    def notice(self):
        
        self.game.update(currentDate = datetime.date.today())
        if (self.lowerPrice == self.currentPrice) \
            and (type(self.game[0].currentPrice) == type(None) or (self.game[0].currentPrice > self.currentPrice)):
            txt = 'buy: ' + self.game[0].name + ' ' + str(self.currentPrice) + '\n' + self.game[0].tbUrl
            email.add_mail_item(subject='买游戏', topic='买游戏碟', txt=txt, minutes_delay=10, deadline=None, cover=False)
#             sendHotmail = threading.Thread(target=sendMail.sendMail, args=('buy: ' + self.game[0].name + ' ' + str(self.currentPrice), \
#                 'game: ' + self.game[0].tbUrl, 'ming188199@hotmail.com', 'hotmail', False))
            sendHotmail.start()
        if (self.currentPrice >= self.game[0].buyPrice + self.game[0].yj + self.game[0].cb):
            txt = 'sell: ' + self.game[0].name + ' ' + str(self.currentPrice) + '\n' + self.game[0].tbUrl
            email.add_mail_item(subject='卖游戏', topic='卖游戏碟', txt=txt, minutes_delay=10, deadline=None, cover=False)
#             sendHotmail = threading.Thread(target=sendMail.sendMail, args=('sell: ' + self.game[0].name + ' ' + str(self.currentPrice), \
#                 'game: ' + self.game[0].tbUrl, 'ming188199@hotmail.com', 'hotmail', False))
#             sendHotmail.start()
            