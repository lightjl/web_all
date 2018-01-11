#-*- encoding: utf-8 -*-
#-*- encoding: gbk -*-

import emailAccount
from imbox import Imbox
import imaplib
import logging
import time
import datetime


# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')



'''
messages_folder = eBox.messages(folder='xiaoshuo')


for uid, message in messages_folder:
# Every message is an object with the following keys
    print(message.subject)
    print((message.body)['plain'])
    eBox.move(uid, 'others')
'''
def Ebox():
    eBox = Imbox('imap-mail.outlook.com',
                    username=emailAccount.hotname,
                    password=emailAccount.hotpass,
                    ssl=True,
                    ssl_context=None)
    return eBox

def delMail(eBox, folder='Sent'):
    messages_folder = eBox.messages(folder=folder)
    for uid, message in messages_folder:
    # Every message is an object with the following keys
        logging.debug(message.subject)
        eBox.delete(uid)

def delMailLt(eBox, folder='Sent', days=15):
    date__lt=datetime.date.today()-datetime.timedelta(days=15)
    messages_folder = eBox.messages(folder=folder, date__lt=date__lt)
    for uid, message in messages_folder:
    # Every message is an object with the following keys
        logging.debug(message.subject)
        eBox.delete(uid)
        
def markReaded(emailbox, folder):
    messagesToRead = emailbox.messages(folder=folder, unread=True)
    for uid, message in messagesToRead:
    # Every message is an object with the following keys
        logging.info(message.subject)
        emailbox.mark_seen(uid)

def moveMail(subject, fromFolder, toFolder):
    eBox = Imbox('imap-mail.outlook.com',
        username=emailAccount.hotname,
        password=emailAccount.hotpass,
        ssl=True,
        ssl_context=None)
    messages_folder = eBox.messages(folder=fromFolder, subject=subject)
    
    for uid, message in messages_folder:
    # Every message is an object with the following keys
        logging.debug(message.subject)
        eBox.move(uid, toFolder)
    eBox.logout()
    
def moveMailUid(mailuid, fromFolder, toFolder):
    eBox = Imbox('imap-mail.outlook.com',
        username=emailAccount.hotname,
        password=emailAccount.hotpass,
        ssl=True,
        ssl_context=None)
    messages_folder = eBox.messages(folder=fromFolder)
    
    for uid, message in messages_folder:
    # Every message is an object with the following keys
        if uid == mailuid:
            logging.debug(message.subject)
            eBox.move(uid, toFolder)
    eBox.logout()
    
def checkMailList(folder, unreadFlag=False):
    checkFlag = True
    list_mail = []
    while checkFlag:
        try:
            checkFlag = False
            eBox = Imbox('imap-mail.outlook.com',
                    username=emailAccount.hotname,
                    password=emailAccount.hotpass,
                    ssl=True,
                    ssl_context=None)
            messages_folder = eBox.messages(folder=folder, unread=unreadFlag)
            for uid, message in messages_folder:
            # Every message is an object with the following keys
                logging.debug(message.subject)
                list_mail.append(message.subject)
                # print((message.body)['plain'])
            eBox.logout()
        except:
            time.sleep(10)
            checkFlag = True
        
    return list_mail

def checkMailFolderList(folderlist):
    eBox = Imbox('imap-mail.outlook.com',
        username=emailAccount.hotname,
        password=emailAccount.hotpass,
        ssl=True,
        ssl_context=None)
    list_mail = []
    for folder in folderlist:
        messages_folder = eBox.messages(folder=folder)
        for uid, message in messages_folder:
        # Every message is an object with the following keys
            logging.debug(message.subject)
            list_mail.append(message.subject)
            # print((message.body)['plain'])
    eBox.logout()
    return list_mail
