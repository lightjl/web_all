import sys
sys.path.append('..')

from common.sendMail import imMail
from django.http import HttpResponse
from moivesDownload.models import Moive, People, Watch, Statue_dm

def fixList(fold, mean, p, unreadFlag=False):
    downloaded = imMail.checkMailList(fold, unreadFlag=unreadFlag)
    for mv in downloaded:
        name = mv[3:]
        mvs = Moive.objects.filter(name_En=name)
        if len(mvs) == 0:
            continue
        mv = mvs[0]
        st = Statue_dm.objects.filter(means=mean)[0]
        ws = Watch.objects.filter(moive=mv)
        if (len(ws) > 0):   #已存在记录
            ws[0].statue=st
            ws[0].save()
        else:
            w = Watch(people=p, moive=mv, statue=st)
            w.save()

def fixDatebase(request):
    p = People.objects.filter(name='me')[0]
    fixList('downloaded', "已下载", p, unreadFlag=True)
    #fixList('mv', "不下载", p)
    fixList('downloading', "要下载", p)
        
    return HttpResponse("fixed")


if __name__ == '__main__':
    #sendedList = imMail.checkMailFolderList(['mv', 'downloaded', 'downloading'])
    donnotDownloadMvs = imMail.checkMailList('downloaded')
    for mv in donnotDownloadMvs:
        name = mv[3:]
        print(name)