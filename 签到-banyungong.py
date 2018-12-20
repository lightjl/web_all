
# coding: utf-8

# In[1]:


from selenium import webdriver
import account

# In[2]:


browser = webdriver.Firefox()
url = 'http://www.banyungong.org/Login.html'
browser.get(url)


# In[3]:


browser.get(url)


# In[4]:


def login(name, password, browser):
    browser.find_element_by_xpath('//*[@id="txtID"]').send_keys(name)
    browser.find_element_by_xpath('//*[@id="txtPass"]').send_keys(password)
    browser.find_element_by_xpath('//*[@id="btnLogin"]').click()


# In[5]:


login(account.byg_name, account.byg_password, browser)


# In[8]:


def qd(browser):
    url = 'http://www.banyungong.org/daysign.html'
    browser.get(url)
    try:
        browser.find_element_by_xpath('//*[@id="btnSign"]').click()
    except:
        return


# In[7]:


qd(browser)

