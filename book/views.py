from django.shortcuts import render, render_to_response
from . import mebook
from django.http import HttpResponse
from book.models import Book
# Create your views here.

def CheckMeBook(request):
    startPage = 1
    endPage = 700
    mebook.mebook(startPage,endPage)
    return HttpResponse('follow %d-%d done' %(startPage, endPage))

def showbook(request):  # show    
    return render_to_response('book/list.html', 
                              {'books':Book.objects.all()
                               })
    
def zzbook(request):  # zz book    
    books = Book.objects.filter(zzFlag = False, rating__gte = 8, id__gte = 6335)
    boosFromDB = mebook.BooksFromDB(books)
    boosFromDB.zzBook()
    return HttpResponse('zz book done')