from django.shortcuts import render,HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from web.reporter import analyzer,read_data
from.models import TourData
from django.db.models import Count,Sum
import datetime


# Create your views here.

def report(request):
  
    left=[]
    height=[]   
    tour_data_query=TourData.objects.all()
    tour_data_groupby=tour_data_query.values('name').annotate(duration_sum=Sum('duration'))
    
    
    chart_data=tour_data_groupby.values_list('name','duration_sum')
    # date1=chart_data[0][2]
    date1='1399/1/2'

 

    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(date1)
    for i in chart_data:
        left.append(i[0])
        height.append(i[1])

    print(left)
    print(height)

    context={
            'labels':left,
            'data':height,
            'date1':date1,
            }
    return render(request,'web/report.html',context)

def import_data():

    tour_data=read_data()

    for row in tour_data:

        obj=TourData(name=row[1],date=row[2],duration=row[3],number=row[4])
        obj.save()   



def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        fs.delete('1.xls')
        filename=fs.save('1.xls',myfile)
        try:
            analyzer()
            import_data()
            
        except :
            return HttpResponse('بارگذاری با خطا مواجه شد')
        
        return HttpResponse('بارگذاری انجام شد')
    return render(request,'web/upload.html')


    
