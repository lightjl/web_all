from control.models import Rask
from multiprocessing import Process, Value
import time
import threading
import logging
import calendar
from datetime import datetime,timedelta,date
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')

class WorkInTime():
    def __init__(self, timeBucket, relaxTime = 60, weekday = 'all'): 
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
        self.time_period = [[datetime.now().strftime('%Y-%m-%d') + ' ' + i for i in timeB] \
                            for timeB in self.__time[:] ]
        logging.debug("WorkInTime init")
    def changeRelaxTime(self, relaxTime):
        logging.debug("changeRelaxTime")
        self.__relaxTime = relaxTime
    def __resetTime(self, id):
        logging.debug("__resetTime")
        r = Rask.objects.filter(id=id)
        self.__time = eval('['+r[0].timePeriod+']')
        
        self.time_period = [[datetime.now().strftime('%Y-%m-%d') + ' ' + i for i in timeB] \
                            for timeB in self.__time[:] ]
    def relaxDay(self, alive):
        #print(self.__today.weekday())
        if self.__weekday == 'All' or self.__weekday == 'all':
            return
        while str(self.__today.weekday()) not in self.__weekday and alive.value:
            self.__today = date.today()
            time.sleep(self.sleep_time)
    # timeTrade = [['9:29', '11:30'], ['13:00', '15:00']]
    
    def relax_during_working_time(self, alive):
        relaxTime = self.__relaxTime
        while alive.value:
            logging.debug('work relaxtime: ' + str(self.sleep_time))
            time.sleep(self.sleep_time)
            relaxTime -= self.sleep_time
            if(relaxTime <= 0):
                break
    
    def relax(self, id, alive, name=''):
        self.relaxDay(alive)  #relaxDay
        self.__resetTime(id)
        while alive.value:
            timeNow = datetime.now().strftime('%Y-%m-%d %H:%M')
            working = False
            for t in self.time_period:
                logging.debug(timeNow)
                logging.debug(name + t[0] + ' ' + t[1])
                # 正常运行
                r = Rask.objects.filter(id=id)
                if t[0] <= timeNow <= t[1]: # 工作时间
                    logging.debug(name + ' relax to work')
                    if r[0].run_time_last.strftime('%Y-%m-%d %H:%M') >= t[0]:# 非第一次运行
                        self.relax_during_working_time(alive) # 中场休息
                    logging.debug(name + ' working')
                    working = True
                    break
                if timeNow > t[0]:
                    if r[0].run_success_time_last.strftime('%Y-%m-%d %H:%M') >= t[0]: #已在该时间段后运行
                        pass
                    else:   # 补运行
                        working = True
                        break
            if working:
                break
            time.sleep(self.sleep_time)


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
    
