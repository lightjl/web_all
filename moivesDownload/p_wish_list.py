from moivesDownload.models import Wish_list
from douban.doubanMoive import DoubanMoive
from vip.models import Moive_vip
from moivesDownload import banyungong, moiveE

def update_wish_list_moive_id():
    w_todo = Wish_list.objects.filter(moive_id = 0)
    for w in w_todo:
        moive_db = DoubanMoive(w.name)
        # update moive_id
        w_tmp = Wish_list.objects.filter(name=w.name)
        w_tmp.update(moive_id = moive_db.moive_id)

def search_moive_byg():
    w_z = Wish_list.objects.filter(watch_status = 'z', moive_id__gt = 0)
    if len(w_z) == 0:
        return
    byg = banyungong.Banyungong()
    myMoives = moiveE.moives()
        
    for w in w_z:
        link = byg.search(w.name)
        if (len(link) > 0):
            mv = moiveE.moiveE(w.name, link)
            myMoives.send(mv)
            w_tmp = Wish_list.objects.filter(name=w.name)
            w_tmp.update(watch_status = 'ZED')
    
    byg.quit()
    


def update_wish_list_watch_status():
    w_z = Wish_list.objects.filter(watch_status = 'z', moive_id__gt = 0)
    moive_id_w_z = [w.moive_id for w in w_z]
    # vip
    m_vip = Moive_vip.objects.filter(moive_id__in = moive_id_w_z, price = 0)
    moive_id_vip = [m.id for m in m_vip]
    print('moive_id_vip', moive_id_vip)
    w_vip = Wish_list.objects.filter(moive_id__in = moive_id_vip)
    w_vip.update(watch_status = 'VIP')



def update_wish_list():
    update_wish_list_moive_id()
    
    update_wish_list_watch_status()
    
    search_moive_byg()
    
update_wish_list()