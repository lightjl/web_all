from multiprocessing import Process
from control import control
import threading
import time
import logging
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')
    
            
c = control.MyControl() #check if it can run
checkRun = threading.Thread(target=c.checkAllTheTime, args=())
checkRun.start()
c.control()
#test = threading.Thread(target=RunRasks, args=(c,))
#test.start()

