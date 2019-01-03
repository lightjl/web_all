import requests
import urllib.request
from bs4 import BeautifulSoup
import time
import random




# -------------------------------------------------------公用方法----------------------------------------------------
class CommanCalss:
    def __init__(self):
        self.header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
        self.testurl='http://www.baidu.com'

    def getresponse(self,url):
        req = urllib.request.Request(url, headers=self.header)
        resp = urllib.request.urlopen(req, timeout=5)
        content = resp.read()
        return content

    def _is_alive(self,proxy):
        try:
            s = requests.Session()
            html = s.get(self.testurl, proxies={"http": proxy}, verify=False, timeout=1)
            if html.status_code == 200:
                return True
        except:
            return False

        return False


# -------------------------------------------------------代理池----------------------------------------------------
class ProxyPool:
    def __init__(self, proxy_finder):
        self.proxy_finder=proxy_finder
        self.pool=[]
        self.alivepool = []
        self.__readTxt()
        self.cominstan=CommanCalss()

    def get_proxies(self):
        self.pool=self.proxy_finder.find()
        for p in self.pool:
            if self.cominstan._is_alive(p):
                # print('alive ' +p)
                self.alivepool.append(p)
            else:
                # print('remove '+p)
                continue

    def fix(self, p):
        if not self.cominstan._is_alive(p):
            self.alivepool.remove(p)
    
    def delpool(self, p):
        self.alivepool.remove(p)
            
    def get_one_proxy(self):
        if (len(self.alivepool) > 0):
            return random.choice(self.alivepool)
        print('reflash, please wait')
        self.get_proxies()
        self.writeToTxt()
        print('reflash done')
        return random.choice(self.alivepool)

    def writeToTxt(self):
        try:
            fp = open('./proxy.txt', "w+")
            while (len(self.alivepool) == 0):
                self.get_proxies()
                print('reflash, please wait')
            for item in self.alivepool:
                fp.write(str(item) + "\n")
            fp.close()
        except IOError:
            print("fail to open file")
            
    def __readTxt(self):
        try:
            text = open('./proxy.txt', "r")
            sths = (text.readlines())
            for ith in range(len(sths)):
                self.alivepool.append(sths[ith][:-1])
        except IOError:
            print("fail to open file")


#-------------------------------------------------------获取代理方法----------------------------------------------------
#定义一个基类
class IProxyFinder:
    def __init__(self):
        self.pool = []

    def find(self):
        return

#西祠代理爬取
class XiciProxyFinder(IProxyFinder):
    def __init__(self, url):
        super(XiciProxyFinder,self).__init__()
        self.url=url
        self.cominstan = CommanCalss()

    def find(self):
        content = self.cominstan.getresponse(self.url + str(random.randint(1,20)))
        soup = BeautifulSoup(content,"lxml")
        ips = soup.findAll('tr')
        for x in range(2, len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            if tds == []:
                continue
            ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
            self.pool.append(ip_temp)
        time.sleep(1)
        return  self.pool

class MyProxy:
    def __init(self):
        pass
        
    def get(self, url):
        finder = XiciProxyFinder("http://www.xicidaili.com/wt/")
        ppool_instance = ProxyPool(finder)
        s = requests.Session()
        while True:
            try:
                proxy = ppool_instance.get_one_proxy()
                html = s.get(url, proxies={"http": proxy}, verify=False, timeout=5)
                if html.status_code == 200:
                    ppool_instance.writeToTxt()
                    return html
                else:
                    testhtml = s.get(url)
                    if testhtml.status_code == 200:
                        ppool_instance.delpool(proxy)
            except:
                ppool_instance.fix(proxy)
        
        
#-------------------------------------------------------测试----------------------------------------------------

if __name__ == '__main__':
    finder = XiciProxyFinder("http://www.xicidaili.com/wt/")
    ppool_instance = ProxyPool(finder)
    print(ppool_instance.get_one_proxy())