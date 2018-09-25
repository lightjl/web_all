from email_os.models import Subject, Topic
import datetime


class Email_item():
    def __init__(self, subject, topic, txt, minutes_delay=10, deadline=None, cover=True):
        self.sub = subject
        self.top = topic
        self.txt = txt
        self.mins = minutes_delay
        self.deadline = deadline
        self.cover = cover
        
    def update_sub(self):
        # todo find sub is exits
        self.ss = Subject.objects.filter(name = self.sub)
        delay_until = datetime.datetime.now()+datetime.timedelta(minutes=self.mins)
        if ((self.deadline) and delay_until > self.deadline):
            delay_until = self.deadline
        if (len(self.ss)==0):
            sub = Subject(name=self.sub, minutes_delay=self.mins, deadline=self.deadline,delay_until=delay_until)
            sub.save()
            self.ss = Subject.objects.filter(name = self.sub)
        else:
            self.ss.update(minutes_delay=self.mins, deadline=self.deadline,delay_until=delay_until)
    
    def update_topic(self):
        
#         print('ts:', len(ts))
        if (self.cover):    # 覆盖,直接删除之前topic
            ts = Topic.objects.filter(sub = self.ss[0], name = self.top)
            print('len_ts', len(ts))
            ts.delete()
            
        t = Topic(sub=self.ss[0], name=self.top, cover=self.cover, txt=self.txt)
        print(self.top, self.cover, self.txt)
        t.save()
    
    def update2os(self):
        if ((self.deadline) and self.deadline > datetime.datetime.now()): # 迟来的信息不发
            return
        self.update_sub()
        self.update_topic()
      
class Email_os():
    def __init__(self):
        return
    
    def add_mail_item(self, subject, topic, txt, minutes_delay=10, deadline=None, cover=True):
#         print(subject, topic, txt, minutes_delay, deadline, cover)
        self.item = Email_item(subject, topic, txt, minutes_delay, deadline, cover)
        self.item.update2os()
        print((subject, topic, txt, minutes_delay, deadline, cover))
