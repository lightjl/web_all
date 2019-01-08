from selenium import webdriver
import time
import logging
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

class Utweb:
    def __init__(self, browser):
        self.browser = browser
        self.url = 'http://127.0.0.1:19575/gui/index.html?localauth=localapi370621dc48c451ff:'
        
    def know_button(self):
        xpath = '//*[@id="search-overlay-mask"]/div[3]/i'
        try:
            self.browser.find_element_by_xpath(xpath).click()
        except:
            return
        
    def add_torrent(self, magnet):
        self.browser.get(self.url)
        time.sleep(6)
        self.know_button()
        time.sleep(6)
        add_button_xpath = '//*[@id="auto-upload-btn"]'
        self.browser.find_element_by_xpath(add_button_xpath).click()
        
        time.sleep(4)
        link_xpath = '//*[@id="upload-torrent-modal"]/div[2]/div[2]/div[2]/input'
        self.browser.find_element_by_xpath(link_xpath).send_keys(magnet)
        commit_xpath = '//*[@id="upload-torrent-modal"]/div[2]/div[2]/button'
        self.browser.find_element_by_xpath(commit_xpath).click()
    
    def del_upload(self):
        browser = self.browser
        browser.get(self.url)
        self.know_button()
        xpath = '//div[@id="media-library-content"]/div[@class="media-element"]'
        divs = browser.find_elements_by_xpath(xpath)
        statu = './div/div[2]/div[1]/div[2]/div[1]/div[1]/span'
        del_button = './div/div[2]/div[2]/div[2]/i'
        remove_button = '//*[@id="auto-remove-torrent-btn"]'
        for div_test in divs:
            if ('上' == div_test.find_element_by_xpath(statu).text[0]):
                print(div_test.find_element_by_xpath('./div/div[2]/div[1]/div[1]').text)
                div_test.find_element_by_xpath(del_button).click()
                time.sleep(6)
                browser.find_element_by_xpath(remove_button).click()
        