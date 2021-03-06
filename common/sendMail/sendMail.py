# !/usr/bin/env python3
# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import emailAccount
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime
import email
from email import encoders
import time
from pathlib import Path

sender = 'presouce@163.com'
smtpserver = 'smtp.163.com'


def sendMailPic(sub, context, pic, receiver='ming188199@hotmail.com', sendFrom='hotmail', changeReceiver=False):
    msg = MIMEMultipart('related')
    #msg = MIMEText(context, _subtype='plain',_charset='utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(sub, 'utf-8')
    msgText = MIMEText('<b>'+ context +'</b><br><img src="' + pic +'"><br>','html','utf-8')
    msg.attach(msgText)
    tosendFlag = True

    tryNum = 0
    while tosendFlag:
        try:
            tosendFlag = False
            if sendFrom == 'hotmail':
                smtp = smtplib.SMTP()
                smtp.connect('smtp-mail.outlook.com')
                smtp.ehlo()
                smtp.starttls() 
                smtp.login(emailAccount.hotname, emailAccount.hotpass)
                smtp.sendmail(emailAccount.hotname, receiver, msg.as_string())
                smtp.quit()
            else:
                smtp163 = smtplib.SMTP()
                smtp163.connect('smtp.163.com')
                smtp163.login(emailAccount.username163, emailAccount.password163)
                smtp163.sendmail(emailAccount.username163, receiver, msg.as_string())
                smtp163.quit()
        except Exception as e:
            print(e)
            tosendFlag = True
            if sendFrom == 'hotmail':
                sendFrom = '163'
            else:
                sendFrom = 'hotmail'
                tryNum += 1
                if (changeReceiver or (tryNum > 10)):
                    sendFrom = '163'
                    receiver = emailAccount.username163
                    
def sendMail(sub, context, receiver='ming188199@hotmail.com', sendFrom='hotmail', changeReceiver=False):
    
    msg = MIMEText(context, _subtype='plain',_charset='utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(sub, 'utf-8')
    
    tosendFlag = True

    tryNum = 0
    while tosendFlag:
        try:
            tosendFlag = False
            if sendFrom == 'hotmail':
                smtp = smtplib.SMTP('smtp-mail.outlook.com')
                smtp.ehlo()
                smtp.starttls() 
                smtp.login(emailAccount.hotname, emailAccount.hotpass)
                smtp.sendmail(emailAccount.hotname, receiver, msg.as_string())
                smtp.quit()
            else:
                smtp163 = smtplib.SMTP()
                smtp163.connect('smtp.163.com')
                smtp163.login(emailAccount.username163, emailAccount.password163)
                smtp163.sendmail(emailAccount.username163, receiver, msg.as_string())
                smtp163.quit()
        except Exception as e:
            print(e)
            tosendFlag = True
            if sendFrom == 'hotmail':
                sendFrom = '163'
            else:
                sendFrom = 'hotmail'
                tryNum += 1
                if (changeReceiver or (tryNum > 10)):
                    sendFrom = '163'
                    receiver = emailAccount.username163

def sendToKindle(sub_folder, file_name):
    file_name = file_name + '.txt'
    kindleAddr = 'yamieborn_1@kindle.cn'
    '''
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "convert" + str(datetime.datetime.now())
    msg['From'] = sender
    msg['To'] = "Your Kindle" + "<" + receiver + ">"
    att = MIMEText(open(os.path.join(sub_folder, file_name), 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"' % file_name
    msg.attach(att)
    '''
    #msg = open(os.path.join(sub_folder, file_name), 'rb').read()
    '''
    msg = MIMEText(open(os.path.join(sub_folder, file_name), 'r').read(),'base64', _charset='utf-8')
    msg['Subject'] = "convert" + str(datetime.datetime.now())
    msg['From'] = sender
    msg['To'] = "Your Kindle" + "<" + kindleAddr + ">"
    '''

    msg = open(os.path.join(sub_folder, file_name), 'r', encoding='utf-8').read()

    msg = MIMEText(open(os.path.join(sub_folder, file_name), 'r').read(),'base64', _charset='utf-8')
    msg['Subject'] = Header("convert" + str(datetime.datetime.now()), 'utf-8')

    server = smtplib.SMTP()
    server.connect('smtp.163.com')
    #print("start login")
    server.login(emailAccount.username163, emailAccount.password163)
    #print("start sending email")
    server.sendmail(sender, kindleAddr, msg.as_string())
    server.quit()

def send_attachment_kd(file):
    kindleAddr = 'yamieborn_1@kindle.cn'
    msg = MIMEMultipart()
    print(file.name)
    msg['Subject'] = 'convert: 小说 ' + file.name
    msg['From'] = sender
    msg['To'] = "Your Kindle" + "<" + kindleAddr + ">"
    part = email.mime.base.MIMEBase('application', "octet-stream")
    #fpath=os.path.join(KINDLE_DIR,filename)
    part.set_payload(file.read_bytes())
    encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment', filename=file.name)
    msg.attach(part)

    server=smtplib.SMTP()
    server.connect('smtp.163.com')
    mailname = emailAccount.sjmail
    mailpass = emailAccount.sjpass

    #mailname = emailAccount.username163
    #mailname = emailAccount.password163
    '''
    mailname = emailAccount.icloudname
    mailpass = emailAccount.icloudpass
    server.connect('smtp.mail.me.com')
    server.ehlo()
    server.starttls()

    mailname = emailAccount.hotname
    mailpass = emailAccount.hotpass
    server.connect('smtp-mail.outlook.com')
    server.ehlo()
    server.starttls() 
    '''

    server.login(mailname, mailpass)
    server.sendmail(mailname, kindleAddr, msg.as_string())
    server.quit()
    file.unlink()
    
    print("Send %s successfully" % file.name)

'''
sub_folder = os.path.join(os.getcwd(), "/xs/")
send_attachment_kd(sub_folder, '刀镇星河 第一百零五章 雷电一型')
'''
