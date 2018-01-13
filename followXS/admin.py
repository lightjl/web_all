from django.contrib import admin
from followXS.models import Xs, Chapter

# Register your models here.

class XsAdmin(admin.ModelAdmin):
    list_display = ('rask', 'url')
    fields = ('rask', 'url')
    
admin.site.register(Xs, XsAdmin)
admin.site.register(Chapter)