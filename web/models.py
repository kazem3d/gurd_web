from django.db import models
import datetime
from account.models import User

# Create your models here.



class GurdInfo(models.Model):
    name=models.CharField('نام',max_length=50)
    # l_name=models.CharField('نام خانوادگی',max_length=50)
    # d_name=models.CharField('نام پدر',max_length=50)
    # id_num=models.CharField('شماره شناسنامه',max_length=50)
    # id_code=models.CharField('کد ملی',max_length=50)
    # sex=models.CharField('جنسیت',max_length=10)
    # b_date=models.DateField('تاریخ تولد')
    # p_birth=models.CharField('محل تولد',max_length=50)
    # thumbnail=models.ImageField(upload_to='media',null=True,blank=True)

    def __str__(self):
        return '{}  -   {}'.format(self.name )


class TourData(models.Model):
    name=models.CharField('نام',max_length=50)
    date=models.DateField()
    duration=models.IntegerField()
    number=models.IntegerField()
    upload_date=models.DateField('تاریخ آپلود',auto_now_add=True)

    class Meta:
        verbose_name = 'tour data'
        verbose_name_plural = 'tour data'

    def __str__(self):
        return '{}    {}'.format(self.name,self.date)

class Comment(models.Model):
    content=models.TextField('متن',)
    publisher=models.ForeignKey(User, verbose_name="کاربر", on_delete=models.CASCADE)
    publish_date=models.DateTimeField('تاریخ ثبت',auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.content)