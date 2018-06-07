# -*- coding: UTF-8 -*-
from moivesDownload.models import Moive, People, Watch, Statue_dm
import logging


# 判断一个unicode是否是英文字母
def is_alphabet(uchar):  
    if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
        return True
    elif ('a' <= uchar <= 'z') or ('A' <= uchar <= 'Z'):
        return True
    else:
        return False
    
def is_punctuations(uchar):
    punctuations_list = ['.', '-', '\'']
    if (uchar in punctuations_list):
        return True
    else:
        return False

class moives:
    def __init__(self):
        #self.sendedList = imMail.checkMailFolderList(['mv', 'downloaded', 'downloading'])
        #logging.debug(self.sendedList)
        self.people = People.objects.filter(name='me')[0]
        pass
    
    def Mv(self, moiveE):
        mv = Moive(name_Zh=moiveE.nameOrigin, name_En = moiveE.nameEnglish, downloadLink = moiveE.ed2kLink)
        mv.save()
        return mv
    
    def saveW(self, mv):
        st = Statue_dm.objects.filter(means="可下载")[0]
        w = Watch(people=self.people, moive=mv, statue=st)
        w.save()
    
    def send(self, moiveE):
        #if (moiveE.nameEnglish in self.sendedList):
        #    return
        if moiveE.ed2k:
            mvs = Moive.objects.filter(name_En=moiveE.nameEnglish)
            if (len(mvs) > 0):
                # print(mvs[0])
                ws = Watch.objects.filter(moive=mvs[0])
                if (len(ws) > 0):
                    return
                else:
                    #print(mvs)
                    logging.critical(moiveE.nameEnglish + ' ' + moiveE.nameOrigin)
                    self.saveW(mvs[0])
            else:
                logging.critical(moiveE.nameEnglish + ' ' + moiveE.nameOrigin)
                self.saveW(self.Mv(moiveE))
            #self.sendedList.append(moiveE.nameEnglish)
            #sendMail.sendMail(moiveE.nameEnglish, moiveE.ed2kLink)#, receiver='presouce@163.com', sendFrom='163')
            
    
    def checkFailedNotice(self):
        sendMail.sendMail("check mv failed!!!!!!!!!!!", "check mv failed!!!!!!!!!!!")
    
    def downloaded(self, nameEnglish):
        pass
        # imMail.moveMail(nameEnglish, 'downloading', 'downloaded')

class NameEng:
    def __init__(self, nameOrigin):
        nameEnglish = ''
        nameBegin = False
        for i in nameOrigin:
            if(is_alphabet(i)):
                nameBegin = True
            if nameBegin:
                if(i.isdigit() or is_alphabet(i) or is_punctuations(i)):
                    nameEnglish += i
                else:
                    break
        self.name = nameEnglish

class moiveE:
    def __init__(self, nameOrigin, ed2kLink):
        self.nameOrigin = nameOrigin
        self.ed2kLink = ed2kLink
        self.nameEnglish = NameEng(nameOrigin).name
        if ed2kLink.startswith('ed2k') or ed2kLink.startswith('magnet:'):
            self.ed2k = True
        else:
            self.ed2k = False
        
    def display(self):
        print(self.nameEnglish + " " + self.nameOrigin)
        if self.ed2k:
            print(self.ed2kLink)
        else:
            print('not ed2k')