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
    list_display = ('name', 'gzFlag', 'ce', 'lowerPrice', 'lowerDate', 'buyPrice', 'currentDate')
    fields = ('gzFlag', 'name', 'url', 'tbUrl', 'buyPrice', 'yj', 'cb', 'currentDate')
    
admin.site.register(zdmWeb, zdmWebAdmin)
admin.site.register(zdmSp, zdmSpAdmin)
admin.site.register(mmmGame, mmmGameAdmin)
