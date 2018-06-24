
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