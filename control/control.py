from control.models import Rask
from multiprocessing import Process, Value
import time
import requests
import threading
import logging
import calendar
from datetime import datetime,timedelta,date
from control.WorkInTime import WorkInTime


        

class MyControl:    #check if it can run
    def __init__(self):
        self.runable = dict()
        self.timeB = dict()
        self.wk = dict()
    
    def check(self):
        for r in Rask.objects.all():
            if not self.runable.get(r.id):
                self.runable[r.id] = Value('b', r.runFlag)
            else:
                self.runable[r.id].value = r.runFlag
            if not self.timeB.get(r.id):
                self.timeB[r.id] = eval('['+r.timePeriod+']')
                self.wk[r.id] = WorkInTime(self.timeB[r.id], r.timeRelax, weekday=r.weekday)
                    
    def checkAllTheTime(self):
        while True:
            self.check()
            time.sleep(5)
    
    def run(self, id, name, webSite):
        while True:
            while self.runable[id].value:
                relaxNow = threading.Thread(target=self.wk[id].relax, args=(self.runable[id], name))
                relaxNow.start()
                logging.debug(name)
                relaxNow.join()
                session = requests.Session()
                session.get(webSite)
            time.sleep(10)
    
    def control(self):
        self.check()
        for r in Rask.objects.all():
            runRask = threading.Thread(target=self.run, args=(r.id, r.name, r.webSite))
            runRask.start()
        
    
'''
v=Value('b', True)
m=MyRask(v,1)
rask = Rask.objects.get(id=1)
timeB = eval('['+rask.timePeriod+']')
print(timeB)
wk = WorkInTime(timeB, rask.timeRelax, weekday=rask.weekday)
wk.changeRelaxTime(89)
wk.relax(v, rask.name)
relaxNow = threading.Thread(target=wk.relax, args=(v, rask.name))
#relaxNow.start()
#login_session = requests.Session()
#login_session.get(rask.webSite)
'''