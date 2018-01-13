from control.models import Rask
from multiprocessing import Process, Value
import time
import requests
import threading
import logging
import calendar
from datetime import datetime,timedelta,date
from control.WorkInTime import WorkInTime
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')


        

class MyControl:
    def __init__(self):
        self.runable = dict()
    
    def check(self):
        while True:
            for r in Rask.objects.all():
                self.runable[r.id] = Value('b', r.runFlag)
            time.sleep(5)
            
def testFun(a, b):
    print("testFun")

class MyRask:
    def __init__(self, runFlag, id):
        self.runFlag = runFlag
        self.rask = Rask.objects.get(id=id)
    
    def run(self):
        while self.runFlag.value:
            
            timeB = eval('['+self.rask.timePeriod+']')
            print(timeB)
            wk = WorkInTime(timeB, self.rask.timeRelax, weekday=self.rask.weekday)
            relaxNow = threading.Thread(target=wk.relax, args=(self.runFlag, self.rask.name))
            relaxNow.start()
            logging.debug(self.rask.name)
            relaxNow.join()
            login_session = requests.Session()
            login_session.get(self.rask.webSite)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/mj.pyrunable.txt'
    file_object = open(filename, 'r')
    try:
        flag_run = file_object.read()
    finally:
        file_object.close()
    while flag_run == 'True':
        time.sleep(5)
        file_object = open(filename, 'r')
        try:
            flag_run = file_object.read()
        finally:
            file_object.close()
    runFlag.value = False
    
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