from django.contrib import admin

# Register your models here.

from smzdm.models import zdmWeb, zdmSp, mmmGame

# Register your models here.

class zdmWebAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'gxFlag')
    fields = ('name', 'url', 'gxFlag')

class zdmSpAdmin(admin.ModelAdmin):
    list_display = ('hwmc','je', 'by', 'mj', 'url', 'zqrq', 'gxsj')
    
class mmmGameAdmin(admin.ModelAdmin):
    list_display = ('name', 'gzFlag', 'lowerPrice', 'lowerDate', 'buyPrice', 'currentPrice', 'currentDate')
    
admin.site.register(zdmWeb, zdmWebAdmin)
admin.site.register(zdmSp, zdmSpAdmin)
admin.site.register(mmmGame, mmmGameAdmin)
