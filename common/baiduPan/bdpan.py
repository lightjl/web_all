import account
from selenium import webdriver
import time

class BaiduPan:
    def __init__(self, browser):
        self.browser = browser

    def login(self):
        self.browser.get('https://pan.baidu.com')
        time.sleep(4)
        # //*[@id="login-middle"]/div/div[6]/div[2]/a
        time.sleep(19)
        self.browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__footerULoginBtn"]').click()
        time.sleep(2)
        # //*[@id="TANGRAM__PSP_4__userName"]
        self.browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__userName"]').send_keys(account.accountbd)
        # //*[@id="TANGRAM__PSP_4__password"]
        self.browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__password"]').send_keys(account.passwordbd)
        # //*[@id="TANGRAM__PSP_4__submit"]
        self.browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__submit"]').click()
        time.sleep(10)
        self.knowButtonClick()
        
    def knowButtonClick(self):
        path_list = ['//p[@class="tip-button"]', '//div[@class="know-button"]']
        for path in path_list:
            try:
                self.browser.find_element_by_xpath(path).click()
                time.sleep(1)
            except:
                pass
    
    def zz(self, link, mm=None):
        self.browser.get(link)
        if mm:
            self.browser.find_element_by_xpath('//*[@id="fkbQ5Wq"]').send_keys(mm)
            self.browser.find_element_by_xpath('//*[@id="uivs0k6Q"]/a/span').click()
        time.sleep(4)
        # choose all
        self.browser.find_element_by_xpath('//*[@id="shareqr"]/div[2]/div[2]/div/ul[1]/li[1]/div').click()
        # save
        self.browser.find_element_by_xpath('//*[@id="bd-main"]/div/div[1]/div/div[2]/div/div/div[2]/a[1]/span/span').click()
        time.sleep(6)
        # sure
        try:
            self.browser.find_element_by_xpath('//*[@id="fileTreeDialog"]/div[4]/a[2]/span/span').click()
        except:
            self.browser.find_element_by_xpath('//*[@id="fileTreeDialog"]/div[3]/a[2]/span/span').click()
        