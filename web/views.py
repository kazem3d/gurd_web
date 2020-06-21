from django.shortcuts import render,HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from web.reporter import analyzer,read_data
from.models import TourData
from django.db.models import Count,Sum


# Create your views here.



def report(request):
    # try:
    #     (left,height)=analyzer()
    #     context={
    #             'labels':left,
    #             'data':height
    #             }

    # except :
    #     context={}

    left=[]
    height=[]   
    tour_data=TourData.objects.all()
    tour_data=tour_data.annotate(duration_sum=Sum('number'))
    data=tour_data.values_list('name','duration_sum')

    for i in data:
        left.append(i[0])
        height.append(i[1])

    print(left)
    print(height)

    context={
            'labels':left,
            'data':height
            }
    return render(request,'web/report.html',context)
    



def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        fs.delete('1.xls')
        filename=fs.save('1.xls',myfile)
        return HttpResponse('بارگذاری انجام شد')
    return render(request,'web/upload.html')

def import_data(request):

    tour_data=read_data()

    for row in tour_data:

        obj=TourData(name=row[1],date=row[2],duration=row[3],number=row[4])
        obj.save()
    
    return HttpResponse('import done')
