from django.contrib import admin
from django.urls import path
from .views import report,upload,import_data

app_name='web'
urlpatterns = [
    path('', report ,name='report'),
    path('upload/', upload,name='upload'),
   
]