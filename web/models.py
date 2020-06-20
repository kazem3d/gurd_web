from django.db import models

# Create your models here.



# class Info(models.Model):
#     f_name=models.CharField('نام',max_length=50)
#     l_name=models.CharField('نام خانوادگی',max_length=50)
#     d_name=models.CharField('نام پدر',max_length=50)
#     id_num=models.CharField('شماره شناسنامه',max_length=50)
#     id_code=models.CharField('کد ملی',max_length=50)
#     sex=models.CharField('جنسیت',max_length=10)
#     b_date=models.DateField('تاریخ تولد')
#     p_birth=models.CharField('محل تولد',max_length=50)
#     thumbnail=models.ImageField(upload_to='media',null=True,blank=True)

#     def __str__(self):
#         return '{}  -   {}'.format(self.f_name , self.l_name)

