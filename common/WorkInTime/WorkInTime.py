from datetime import *
import calendar
from datetime import datetime,timedelta
import time
from multiprocessing import Value
import logging

#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')
#timeBucket=[[时间起，时间止]，[时间点]*2]
#从小到大排序，不支持跨日
class WorkInTime():
    def __init__(self, timeBucket, relaxTime=60, addTime=4.6, weekday='All'):    #工作时间段和冗余时间,run weekday
        self.__time = timeBucket
        self.__weekday = weekday
        self.sleep_time = 60
        now = datetime.now()
        self.__timeType = [[time.mktime(time.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day) +\
                            ' ' + i + ':00', '%Y-%m-%d %H:%M:%S')) for i in timeB] for timeB in self.__time[:]
                         ]

        self.__timeType233 = [[i for i in timeB] for timeB in self.__time[:]
                         ]
        self.__addTime = addTime      #冗余时间
        self.__relaxTime = relaxTime    #休息时间
        self.__newday = True
        self.__today = date.today()
        self.fromWitch = -2 # 从哪个休息区来 , -2为未初始化

    def changeRelaxTime(self, relaxTime):
        self.__relaxTime = relaxTime    #休息时间

    def __resetTime(self):
        now = datetime.now()
        self.__today = date.today()
        self.__timeType = [[time.mktime(time.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day) +\
                            ' ' + i + ':00', '%Y-%m-%d %H:%M:%S')) for i in timeB] for timeB in self.__time[:]
                         ]
    def relaxDay(self, alive):
        #print(self.__today.weekday())
        if self.__weekday == 'All':
            return
        while str(self.__today.weekday()) not in self.__weekday and alive.value:
            self.__today = date.today()
            time.sleep(self.sleep_time)

    # timeTrade = [['9:29', '11:30'], ['13:00', '15:00']]
    def relax(self, alive, name=''):
        self.relaxDay(alive)  #relaxDay
        timeBucket = self.__timeType
        fromRelaxFlag = False
        while alive.value:
            timeNow = time.time()
            #logging.debug(name)
            working = False
            if (timeNow > timeBucket[-1][1]):      #大于一天终止时间
                logging.debug(name + '大于一天终止时间 time relax')
                time.sleep(self.sleep_time)
                logging.debug(name + '大于一天终止时间 time out')
                self.__resetTime()
                timeBucket = self.__timeType
                if (self.fromWitch != -1):  #错过最后一班车
                    self.fromWitch = -1
                    break
            elif timeNow < timeBucket[0][0]:      #小于一天开始时间
                logging.debug(name + '小于一天开始时间 time relax')
                time.sleep(self.sleep_time)
                logging.debug(name + '小于一天开始时间 time out')
                fromRelaxFlag = True
                self.fromWitch = 0  #还没开始发车
            else:
                for i in range(len(timeBucket)-1)[::-1]:
                    if (timeNow > timeBucket[i][1] and timeNow < timeBucket[i+1][0]):
                        logging.debug(name + '中场 time relax')
                        time.sleep(self.sleep_time)
                        logging.debug(name + '中场 time out')
                        fromRelaxFlag = True
                    elif (timeNow <= timeBucket[i][1] and timeNow >= timeBucket[i][0]):
                           #工作区
                        working = True
                        self.fromWitch = i+1  #第n个工作周期
                        break
                if(timeNow >= timeBucket[-1][0] and timeNow <= timeBucket[-1][1]):
                       #最后一个工作区
                    working = True
            if(working):
                break
        relaxTime = self.__relaxTime
        logging.debug(name + 'work relax')
        while alive.value:
            if fromRelaxFlag:   # 睡毛线，起来工作
                break
            time.sleep(self.sleep_time)
            relaxTime -= self.sleep_time
            logging.debug(name + 'work relaxtime: ' + str(relaxTime))
            if(relaxTime < 0):
                break
        logging.debug(name + 'working')


'''
wt = WorkInTime([['12:00', '12:00']], weekday='3')
wt.relaxDay()
wt = WorkInTime([['12:00', '12:00']], weekday='2,3')
wt.relaxDay()
wt = WorkInTime([['12:00', '12:00']])
wt.relaxDay()

a = Value('b', True)
wt = WorkInTime([['15:00', '15:10'], ['15:37', '15:37']])
logging.info('time relax')
wt.relax(a)
logging.info('time out')
'''
