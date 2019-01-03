from django.shortcuts import render
from django.http import HttpResponse
from . import p_qieman
# Create your views here.

def check(request):
    e_big = p_qieman.longwin_detail()
    me = p_qieman.longwin_detail_my()
    d = p_qieman.Fund_deal()
    d.deal()
    d.buy()
    
    return HttpResponse('follow qieman done')