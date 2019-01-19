from selenium import webdriver
import re
import time
from xmjqd.models import gsy
import datetime
from django.db.models import Min
from lxml import etree
import requests
from common.sendMail import sendMail
import threading
from email_os import p_email_os
import logging

class item_gsy:
    def __init__(self, browser):
        self.browser = browser
    
    def nl(self, nl_str):
        self.nlq = nl_str[0]
        if nl_str[1] == '岁':
            self.nlz = 12
        else:
            self.nlz = nl_str[2]
            
    def count_bfl_w(self, bfl_str):
        bfl = bfl_str[:-1]
        if bfl_str[-1] == '千':
            return int(bfl)/10
        if bfl_str[-1] == '亿':
            return int(bfl)*10000
        return int(bfl)
    
    def find_items(self):
        #             //*[@id="app"]/div[2]/div/div[1]/div[2]/div[1]/span[1]
        name_xpath = '//*[@id="app"]/div[2]/div/div[1]/div[2]/div[1]/span[1]'
        lb_xpath = '//*[@id="app"]/div[2]/div/div[1]/div[2]/div[2]/span[2]'
        sl_xpath = '//*[@id="app"]/div[2]/div/div[1]/div[2]/div[1]/span[2]' # (30首)
        nl_xpath = '//*[@id="app"]/div[2]/div/div[1]/div[2]/div[2]/span[5]'
        
        bfl_w_xpath = '//*[@id="app"]/div[2]/div/div[1]/div[2]/div[2]/span[7]' # 274万+
        bz_xpath = '//*[@id="app"]/div[2]/div/div[1]/div[2]/div[3]' 
        self.url = self.browser.current_url  
#         print(self.url)
        
        self.name = self.browser.find_element_by_xpath(name_xpath).text
        self.lb    =    self.browser.find_element_by_xpath(lb_xpath).text
        self.sl    =    self.browser.find_element_by_xpath(sl_xpath).text[1:-2]
        nl_str = self.browser.find_element_by_xpath(nl_xpath).text
        self.nl(nl_str)
        bfl_str    =    self.browser.find_element_by_xpath(bfl_w_xpath).text[:-1]
        self.bfl_w = self.count_bfl_w(bfl_str)
        self.bz    =    self.browser.find_element_by_xpath(bz_xpath).text
        print(self.name, self.nlq, self.nlz, self.lb, self.sl, self.bfl_w, self.bz)
        item = gsy(name = self.name, lb = self.lb, sl = self.sl, nlq = self.nlq, nlz = self.nlz\
                   ,bfl_w = self.bfl_w, url = self.url, bz = self.bz)
        item.save()
        
    def exits(self, url):
        items = gsy.objects.filter(name = url)
        if (len(items)>0):
            return True
        return False

class p_gsy:
    def __init__(self):
        self.url = 'http://www.jiqid.com/downloadres/'
    
    def check(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        self.item = item_gsy(self.browser)
        lb_xpath = '//*[@id="app"]/div[2]/div[2]/div/div[1]/div'
        lbs = self.browser.find_elements_by_xpath(lb_xpath)
        for lb in lbs[:-1]:
            lb.click()
            self.check_lb()
        self.browser.quit()
        
    def check_lb(self):
        next_page_xpath = '//div[@class="list_arrow next"]'

        time.sleep(4)
        next_page = self.browser.find_element_by_xpath(next_page_xpath)
        next_class = next_page.find_element_by_xpath('../div').get_attribute('class')
        # disabled
        while ('disabled' not in next_class):
            self.check_page()
            next_page.click()
            next_page = self.browser.find_element_by_xpath(next_page_xpath)
            next_class = next_page.find_element_by_xpath('../div').get_attribute('class')
            time.sleep(4)
    
    def check_page(self):
        li_xpath = '//*[@id="type1"]/div/ul/li[*]'
        lis = self.browser.find_elements_by_xpath(li_xpath)
        for li in lis[:]:
            li.click()
            handles = self.browser.window_handles
            self.browser.switch_to_window(handles[-1])
            time.sleep(4)
            # todo 跳过已有项，需增加url判断 self.item.exits
            self.check_item()
            self.browser.close()
            self.browser.switch_to_window(handles[0])
            
        
    def check_item(self):     
        self.item.find_items()
