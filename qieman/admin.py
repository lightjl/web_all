from django.contrib import admin

# Register your models here.
from qieman.models import Fund

class FundAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'fs','fs_my', 'yk', 'yk_my'\
                    , 'price_min', 'price_min_my', 'price_hold', 'price_hold_my', 'jz', 'gxsj'\
                    , 'gszzl']

admin.site.register(Fund, FundAdmin)