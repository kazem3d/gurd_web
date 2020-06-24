from django.shortcuts import render,HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from web.reporter import analyzer,read_data
from.models import TourData
from django.db.models import Count,Sum
import datetime
import jdatetime



# Create your views here.

def report(request):
  
    left=[]
    height=[]   
    tour_data_query=TourData.objects.filter(upload_date=datetime.date.today())
    tour_data_groupby=tour_data_query.values('name').annotate(duration_sum=Sum('duration'))
    
    
    chart_data=tour_data_groupby.values_list('name','duration_sum')

    if tour_data_query:
        date=tour_data_query.values_list('date')[0][0]
    else :
        date=jdatetime.date.today()

    for i in chart_data:
        left.append(i[0])
        height.append(i[1])

    print(left)
    print(height)

    context={
            'labels':left,
            'data':height,
            'date':date,
            }
    return render(request,'web/report.html',context)

def import_data():

    tour_data=read_data()

    for row in tour_data:
        
        obj=TourData(name=row[1],date=row[2],duration=int(row[3]),number=row[4])

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
            context={
                'message':'بارگذاری انجام گردید',
                'message_color':'success'
                    }
            
        except :
            context={
                'message':'بارگذاری  با خطا مواجه شد',
                'message_color':'danger'
            }
        

        return render(request,'web/upload.html',context)


    return render(request,'web/upload.html')


def details_report(request)  :

    left=[]
    height=[]

    if request.GET.get('gurd_name'):
        name=request.GET.get('gurd_name')

        tour_data_query=TourData.objects.filter(name__contains=name).order_by('date')

        chart_data=tour_data_query.values_list('date','duration')
        
        for i in chart_data:
            left.append(i[0].strftime("%m-%d"))
            height.append(i[1])


        context={
                'labels':left,
                'data':height,
                'name':name
                }
        return render(request,'web/detail_report.html',context)


    return render(request,'web/detail_report.html')

    

 
