from django.shortcuts import render
from django.http import HttpResponse
from email_os.models import Subject, Topic
import datetime
from common.sendMail import sendMail
import threading


# Create your views here.
# Create your views here.

def check(request):
    mailFlag = True
    mymail = Subject.objects.filter(delay_until__lte = datetime.datetime.now())
    for sub in mymail:
        txt_objs = Topic.objects.filter(sub = sub)
        texts = '\n\n'.join(t.txt for t in txt_objs)
#         print(texts)
        if mailFlag:
            sendHotmail = threading.Thread(target=sendMail.sendMail,\
                args=(sub.name\
                    ,texts, 'ming188199@hotmail.com', 'hotmail', False))
            sendHotmail.start() # 邮件通知
#             sendMail.sendMail(sub.name, texts, changeReceiver=True)
            sub.delete()
    
    return HttpResponse('check mail done')