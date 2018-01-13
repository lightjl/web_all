from multiprocessing import Process
from control import control
import threading
import time
import common.WorkInTime
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')
    

def RunRasks(c):
    rasks = dict()
    while True:
        for (id,v) in c.runable.items():
            if not rasks.get(id):
                logging.debug("new rask")
                rasks[id] = control.MyRask(v, id)
                runRask = threading.Thread(target=rasks[id].run, args=())
                runRask.start()
        time.sleep(60)
            
        
c = control.MyControl()
checkRun = threading.Thread(target=c.check, args=())
checkRun.start()

#test = threading.Thread(target=RunRasks, args=(c,))
#test.start()


RunRasks(c)
