from django.contrib import admin
from django.urls import path
from .views import report,upload,import_data,details_report,comment,date_report,compare_report

app_name='web'
urlpatterns = [
    path('', report ,name='report'),
    path('upload/', upload,name='upload'),
    path('details_report/', details_report,name='details_report'),
    path('comment/', comment,name='comment'),
    path('compare_report/', compare_report,name='compare_report'),
    path('date_report/', date_report,name='date_report'),


   
]