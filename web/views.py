from django.shortcuts import render,HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from web.reporter import analyzer


# Create your views here.



def report(request):
    try:
        (left,height)=analyzer()
        context={
                'labels':left,
                'data':height
                }

    except :
        context={}

        
    return render(request,'web/report.html',context)

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        fs.delete('1.xls')
        filename=fs.save('1.xls',myfile)
        return HttpResponse('بارگذاری انجام شد')
    return render(request,'web/upload.html')
