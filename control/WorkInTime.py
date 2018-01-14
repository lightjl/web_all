from control.models import Rask
from multiprocessing import Process, Value
import time
import threading
import logging
import calendar
from datetime import datetime,timedelta,date

class WorkInTime():
    def __init__(self, timeBucket, relaxTime, weekday): 
        self.__time = timeBucket
        self.__weekday = weekday
        self.sleep_time = min(60, relaxTime)
        now = datetime.now()
        self.__timeType = [[time.mktime(time.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day) +' ' + i + ':00', '%Y-%m-%d %H:%M:%S')) for i in timeB] for timeB in self.__time[:] ]
        # self.timeType233 = [[i for i in timeB] for timeB in self.__time[:]]
        # self.addTime = 4.6
        self.__relaxTime = relaxTime
        self.__newday = True
        self.__today = date.today()
        self.fromWitch = -2 # from where -2 first time
        self.fromRelaxFlag = True
        logging.debug("WorkInTime init")
    def changeRelaxTime(self, relaxTime):
        logging.debug("changeRelaxTime")
        self.__relaxTime = relaxTime
    def __resetTime(self):
        logging.debug("__resetTime")
        now = datetime.now()
        self.__today = date.today()
        self.__timeType = [[time.mktime(time.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day) +\
                            ' ' + i + ':00', '%Y-%m-%d %H:%M:%S')) for i in timeB] for timeB in self.__time[:]
                         ]
    def relaxDay(self, alive):
        #print(self.__today.weekday())
        if self.__weekday == 'All' or self.__weekday == 'all':
            return
        while str(self.__today.weekday()) not in self.__weekday and alive.value:
            self.__today = date.today()
            time.sleep(self.sleep_time)
    # timeTrade = [['9:29', '11:30'], ['13:00', '15:00']]
    def relax(self, alive, name=''):
        self.relaxDay(alive)  #relaxDay
        timeBucket = self.__timeType
        while alive.value:
            timeNow = time.time()
            #logging.debug(name)
            working = False
            if (timeNow > timeBucket[-1][1]):      # 
                self.fromRelaxFlag = True
                if (self.fromWitch != -1):  # miss last one 
                    self.fromWitch = -1
                    break
                logging.debug(name + ' bigger than last one time relax')
                time.sleep(self.sleep_time)
                logging.debug(name + ' bigger than last one time out')
                self.__resetTime()
                timeBucket = self.__timeType
            elif timeNow < timeBucket[0][0]:      #
                logging.debug(name + ' smaller than first time relax')
                time.sleep(self.sleep_time)
                logging.debug(name + ' smaller than first time out')
                self.fromWitch = 0  #before first one
                self.fromRelaxFlag = True
            else:
                for i in range(len(timeBucket)-1)[::-1]:
                    if (timeNow > timeBucket[i][1] and timeNow < timeBucket[i+1][0]):
                        print(self.fromWitch)
                        if(self.fromWitch != i+1):  # last work time
                            self.fromWitch = i+1
                            working = True
                            break
                        logging.debug(name + ' mid time relax')
                        time.sleep(self.sleep_time)
                        logging.debug(name + ' mid time out')
                        self.fromRelaxFlag = True
                    elif (timeNow <= timeBucket[i][1] and timeNow >= timeBucket[i][0]):
                        working = True
                        self.fromWitch = i+1  #nth working
                        break
                if(timeNow >= timeBucket[-1][0] and timeNow <= timeBucket[-1][1]):
                    # last work
                    self.fromWitch = -1
                    working = True
            if(working):
                break
        relaxTime = self.__relaxTime
        while alive.value:
            if self.fromRelaxFlag:   #
                self.fromRelaxFlag = False
                break
            logging.debug(name + ' work relaxtime: ' + str(relaxTime))
            time.sleep(self.sleep_time)
            relaxTime -= self.sleep_time
            if(relaxTime <= 0):
                break
        logging.debug(name + ' working')


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
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')
    wt = WorkInTime([['14:45']*2,['14:46']*2])
    wt = WorkInTime([['15:06', '15:07'], ['15:08']*2 ])
    wt = WorkInTime([['15:27']*2 ])
    runFlag = Value('b', True)
    logging.critical('beg:' +  datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    while True:
        wt.relax(runFlag)
        logging.critical('work:' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
