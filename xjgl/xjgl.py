import json
import requests
#from datetime import datetime as dt
import os
import time
from common.sendMail import sendMail
import logging
from xjgl.models import Nhg
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')

def watch(id):
    nhg = Nhg.objects.get(id=id)
    logging.info("现金管理正在运行")
    if (nhg.setDate != datetime.date.today()):  #Init today
        if (datetime.datetime.now().weekday() == 4): #仅考虑1天逆回购
            nhg.highTodayInit = nhg.highInit*3
        elif(datetime.datetime.now().weekday() == 3): #逆回购新规占用天数
            nhg.highTodayInit = nhg.highInit*0.75
        else:
            nhg.highTodayInit = nhg.highInit
        nhg.highest = nhg.highTodayInit
        nhg.save()
    try:
        check_seesion = requests.Session()
        url = 'https://www.jisilu.cn/data/repo/sz_repo_list/?___t=1489544161142'
        xjglInfo = check_seesion.get(url)
        #print(xjglInfo.content.decode())
        jsonXjgl = json.loads(xjglInfo.content.decode())
    except:
        return
    
    nhg = Nhg.objects.get(id=id)
    row = jsonXjgl['rows'][nhg.row_sz]
    #print(row)
    rowHigh = float(row['cell']['price'])
    if rowHigh > nhg.highest:    #新高超过前基准
        sub = '逆回购: ' + row['id'] + ' 破 ' + str(nhg.highest) + ', 现价: ' + row['cell']['price']
        nhg.highest = max(nhg.highest * 1.3, rowHigh)
        logging.critical(sub)
        sendMail.sendMail(sub, "", changeReceiver=True)
        nhg.save()
        

