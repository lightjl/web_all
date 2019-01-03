from selenium import webdriver
import time
import logging
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

class Utweb:
    def __init__(self, browser):
        self.browser = browser
        
    def add_torrent(self, magnet):
        url = 'http://127.0.0.1:19575/gui/index.html?localauth=localapi370621dc48c451ff:'
        self.browser.get(url)
        time.sleep(6)
        add_button_xpath = '//*[@id="auto-upload-btn"]'
        self.browser.find_element_by_xpath(add_button_xpath).click()
        
        time.sleep(4)
        link_xpath = '//*[@id="upload-torrent-modal"]/div[2]/div[2]/div[2]/input'
        self.browser.find_element_by_xpath(link_xpath).send_keys(magnet)
        commit_xpath = '//*[@id="upload-torrent-modal"]/div[2]/div[2]/button'
        self.browser.find_element_by_xpath(commit_xpath).click()
        
        