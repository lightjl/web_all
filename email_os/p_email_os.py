from email_os.models import Subject, Topic
import datetime


class Email_item():
    def __init__(self, subject, topic, txt, minutes_delay=10, deadline, cover=True):
        self.sub = subjcet
        self.top = topic
        self.txt = txt
        self.mins = minutes_delay
        self.deadline = deadline
        self.cover = cover
        
    def update_sub(self):
        # todo find sub is exits
        self.ss = Subject.objects.filter(name = self.sub)
        delay_until = datetime.datetime.now()+datetime.timedelta(minutes=self.mins)
        if (len(self.ss)==0):
            sub = Subject(name=self.sub, minutes_delay=self.mins, deadline=self.deadline,delay_until=delay_until)
            sub.save()
            self.ss = Subject.objects.filter(name = self.sub)
        else:
            self.ss.update(minutes_delay=self.mins, deadline=self.deadline,delay_until=delay_until)
    
    def update_topic(self):
        ts = Subject.objects.filter(sub = self.ss)
        if (self.cover):
            ts.delete()
        t = Topic(sub=self.ss, name=self.top, cover=self.cover, txt=self.txt)
        t.save()
    
    def update2os(self):
        self.update_sub()
        self.update_topic()