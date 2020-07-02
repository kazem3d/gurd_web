from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from web.reporter import analyzer,read_data
from.models import TourData,Comment
from django.db.models import Count,Sum
import datetime
import jdatetime
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.

def report(request):
  

    comments=Comment.objects.filter(publish_date__gt=datetime.date.today()).order_by('-publish_date')

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
            'comments':comments
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

        tour_data_groupby=tour_data_query.values('date').annotate(duration_sum=Sum('duration'))


        chart_data=tour_data_groupby.values_list('date','duration_sum')
        
        for i in chart_data:
            left.append(i[0].strftime("%m-%d"))
            height.append(i[1])

        #calculating moving avarage
        N = 17
        cumsum, moving_aves = [0], []

        for i, x in enumerate(height, 1):
            cumsum.append(cumsum[i-1] + x)
            if i>=N:
                moving_ave = (cumsum[i] - cumsum[i-N])/N
                #can do stuff with moving_ave here
                moving_aves.append(int(moving_ave))


        context={
                'labels':left,
                'data':height,
                'name':name,
                'avarege':moving_aves
                }
        return render(request,'web/detail_report.html',context)


    return render(request,'web/detail_report.html')

@login_required   
def comment(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            obj=Comment()
            message=form.cleaned_data['content']
            obj.content=message
            obj.publisher=request.user
            obj.save()        
            
    
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('web:report'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    return render(request, 'web/comment.html', {'form': form})   
 
def compare_report(request):
    return HttpResponse ('<h1>در دست ساخت</h1>')

def date_report(request):
    return HttpResponse ('<h1>در دست ساخت</h1>')

