from django.contrib import admin
from .models import TourData,Comment
# Register your models here.

class InfoAdmin(admin.ModelAdmin):
    list_display =('name','date','duration','number','upload_date')
    list_filter=('name','date')


admin.site.register(TourData,InfoAdmin)
admin.site.register(Comment)
