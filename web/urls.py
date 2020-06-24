from django.contrib import admin
from django.urls import path
from .views import report,upload,import_data,details_report

app_name='web'
urlpatterns = [
    path('', report ,name='report'),
    path('upload/', upload,name='upload'),
    path('details_report/', details_report,name='details_report'),
   
]