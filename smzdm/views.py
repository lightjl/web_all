from django.shortcuts import render
from smzdm.models import mmmGame
from smzdm.mmmGame import Game
from django.http import HttpResponse
import datetime 
from django.db.models import Q

# Create your views here.

def checkGames(request):
    games = mmmGame.objects.filter(~Q(currentDate = datetime.date.today()), gzFlag = True)
    for game in games:
        gamePriceInfo = Game(game.id)
    return HttpResponse('checked games')
    