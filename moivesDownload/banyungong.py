from selenium import webdriver
import account
import time

from selenium.webdriver.common.keys import Keys

class Banyungong:
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.login()
        pass
    
    def login(self):
        browser = self.browser
        url = 'http://www.banyungong.org/Login.html'
        browser.get(url)
        browser.find_element_by_xpath('//*[@id="txtID"]').send_keys(account.byg_name)
        browser.find_element_by_xpath('//*[@id="txtPass"]').send_keys(account.byg_password)
        browser.find_element_by_xpath('//*[@id="btnLogin"]').click()
        time.sleep(4)
        
    def search(self, name):
        list_fh = [':', '·']
        for fh in list_fh:
            name = name.replace(fh, ' ')
        url = 'http://www.banyungong.org/search/'
        browser = self.browser
        browser.get(url)
        browser.find_element_by_xpath('//*[@id="ucHeader1_txtSearch"]').send_keys(Keys.CONTROL,'a')  
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="ucHeader1_txtSearch"]').send_keys(Keys.SPACE)  
        time.sleep(2)
        
        browser.find_element_by_xpath('//*[@id="ucHeader1_txtSearch"]').send_keys(name)
        browser.find_element_by_xpath('//*[@id="ucHeader1_btnSearch"]').click()
        time.sleep(4)
        # //*[@id="TableList1"]/tbody/tr[2]
        trs = browser.find_elements_by_xpath('//*[@id="TableListTop"]/tbody/tr')
        if (len(trs) == 0):
            trs = browser.find_elements_by_xpath('//*[@id="TableList1"]/tbody/tr')
        
        htmls = []
        for tr in trs[1:]:
            
            fl = tr.find_element_by_xpath('./td[1]/a').text
            if '电影' not in fl and '蓝光' not in fl:
                continue
            name = tr.find_element_by_xpath('./td[2]/a[4]').text
            if 'HD' in name or 'BD' in name:
                htmls.append(tr.find_element_by_xpath('./td[2]/a[4]').get_attribute('href'))
        
        # check all html
        for html in htmls:
            browser.get(html)
            tds = browser.find_elements_by_xpath('//*[@id="pnlD"]/table/tbody/tr/td')
            for td in tds[:2]:
                # //*[@id="btnMagnet"]
                try:
                    td.find_element_by_xpath('./input').click()
                    return browser.find_element_by_xpath('//*[@id="hlkDown"]').get_attribute('href')
                except:
                    continue
        return ''
    
    def quit(self):
        self.browser.quit()