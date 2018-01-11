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
                smtp163.login(emailAccount.username, emailAccount.password)
                smtp163.sendmail(emailAccount.username, receiver, msg.as_string())
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
                    receiver = emailAccount.username
                    
def sendMail(sub, context, receiver='ming188199@hotmail.com', sendFrom='hotmail', changeReceiver=False):
    
    msg = MIMEText(context, _subtype='plain',_charset='utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(sub, 'utf-8')
    
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
                smtp163.login(emailAccount.username, emailAccount.password)
                smtp163.sendmail(emailAccount.username, receiver, msg.as_string())
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
                    receiver = emailAccount.username

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
    server.login(emailAccount.username, emailAccount.password)
    #print("start sending email")
    server.sendmail(sender, kindleAddr, msg.as_string())
    server.quit()

def send_attachment_kd(sub_folder, file_name):
    kindleAddr = 'yamieborn_1@kindle.cn'
    msg = MIMEMultipart()
    msg['Subject'] = 'convert: 小说 ' + file_name
    msg['From'] = sender
    msg['To'] = "Your Kindle" + "<" + kindleAddr + ">"
    part = email.mime.base.MIMEBase('application', "octet-stream")
    #fpath=os.path.join(KINDLE_DIR,filename)
    filename_txt = sub_folder + file_name + ".txt"
    #print filename_txt.decode('utf-8'
    filecontent=open((filename_txt),'rb').read()
    part.set_payload(filecontent)
    encoders.encode_base64(part)

    part.add_header('Content-Disposition', 'attachment', filename=file_name+ '.txt')
    msg.attach(part)

    server=smtplib.SMTP()
    server.connect('smtp.163.com')
    server.login(emailAccount.username, emailAccount.password)
    server.sendmail(sender, kindleAddr, msg.as_string())
    server.quit()
    print("Send %s successfully" % file_name)

'''
sub_folder = os.path.join(os.getcwd(), "/xs/")
send_attachment_kd(sub_folder, '刀镇星河 第一百零五章 雷电一型')
'''