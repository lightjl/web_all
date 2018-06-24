from django.contrib import admin
     
# Register your models here.

from book.models import Book, Read, People, Statue_dm

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('bookname', 'rating', 'tags', 'gxsj', 'cclink', 'dblink')
    # fields = ('bookname', 'rating', 'tags', 'cclink', 'dblink', 'bz')

class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)
    
class ReadAdmin(admin.ModelAdmin):
    list_display = ('people','book', 'statue', 'cs')
    fields = ('people','book','statue', 'cs')
    
admin.site.register(Book, BookAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(Read, ReadAdmin)
admin.site.register(Statue_dm)