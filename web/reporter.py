import sqlite3
import xlrd
from web.gurd import time_dif,similar
import datetime
from difflib import SequenceMatcher,get_close_matches
import csv
import jdatetime


def analyzer():

    #create and connect to report_datebase

    conn=sqlite3.connect('web/report/report_database')
    curser=conn.cursor()

    #create main table in database   
    curser.execute('''

        CREATE TABLE IF NOT EXISTS main (

        id integer PRIMARY KEY,
        name TEXT NOT NULL ,
        tour_date TEXT  ,
        duration TEXT  ,
        number TEXT

        );''')

    #function for writing a tupel in main table
    def record_in_database(data_tupel):

        curser.execute('INSERT INTO main (name,tour_date,duration,number)  VALUES (?,?,?,?)' ,data_tupel)
        conn.commit()


    #function for reading a table from date base and return data of row in list of list
    def read_from_datebase(table_name,order):
        _list=[]
        curser.execute('SELECT * FROM %s ORDER BY %s ' %(table_name,order))
        rows=curser.fetchall()
        for row in rows:
            row=list(row)
            _list.append(row)
        return _list



    #function for removing all rows  from  table of database
    def delete_from_database(tabel_name):
        curser.execute('DELETE FROM \'%s\'; ' %(tabel_name) )
        print('***********************')
        print('tabel main cleared')
        conn.commit()


    #clear database at first
    delete_from_database('main')


    print('Your xls file must be in /files/ folder  ')
    print('File\'s name must be like \"1 (5).xls>\" ')
    print('')


    #Reading xls file and write data in database one by one
    #The format of xls file name must be like <1 (5).xls>
    for m in range(1,2):

        
        # address='web/files/'+'1 ({}).xls'.format(m)
        address='media/1.xls'

        print('*******************************')
        print('Reading: %s' %address[7:])
        print('*******************************')

        #open xls file
        excel_reader=xlrd.open_workbook(address) 
        sheet = excel_reader.sheet_by_index(0) 
        sheet.cell_value(0,0) 

        j=0

        # i start from 2 beacause the first two row dont needed
        i=2

        #counter for counting number of tags that get checked
        tour_counter=0

        #Reading row of xls rows one by one
        while i  < (sheet.nrows):
            
            tour_counter =tour_counter+1    
            print('row id:',i)
            
            #cheking if name row have any data or is empty
            if sheet.row_values(i)[0] != '':

                #scrape name and start time from first row
                if j == 0:
                    
                    name=sheet.row_values(i)[0]

                    #Edit name if has any mistake
                    if similar(name) :
                        name=similar(name)

                    start_time= sheet.row_values(i)[3] 
                    start_time=datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")

                    #converting date to jalali
                    tour_date=jdatetime.datetime.fromgregorian(datetime=start_time)
                    tour_date=tour_date.strftime("%Y-%m-%d")

                    print('name=',name)
                    print('start_time= ',start_time)
                    j=1

                #scrape end time from last row
                elif j == 1:
                    # i-1 because it must returm one row back
                    i=i-1

                    end_time=sheet.row_values(i)[3]
                    end_time=datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")

                    print('end_time= ',end_time)
                    j=3

                #calculate duration of tour from start and end time
                #write a tuple of tour data in database   
                if j == 3:
                    #calculate tour duration from start and end time
                    duration=time_dif(start_time,end_time)

                    print('number of tags that get checked = ',tour_counter-1)
                    print('duration= ',duration)
                    
                    #record a row of data in main table of datebase
                    record_in_database((name,tour_date,int(duration),tour_counter-1))

                    #reset variable for nex loop
                    name=''
                    start_time=''
                    end_time=''
                    tour_date=''
                    j=0
                    tour_counter=0
                    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')


            i+=1 

            #this condition checked if we reach to the end row of xls file  
            if i == sheet.nrows:
                print('row id:',i)

                end_time=sheet.row_values(i-1)[3]
                end_time=datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")
                duration=time_dif(start_time,end_time)

                print('end_time=',end_time)
                print('number of tags that get checked = ',tour_counter)
                print('duration= ',duration)
            
                record_in_database((name,tour_date,int(duration),tour_counter))

                name=''
                start_time=''
                end_time=''
                print('################################')
    curser.execute('DROP TABLE IF EXISTS duration_tour; ')     
    curser.execute('DROP TABLE IF EXISTS number_of_tour; ')     

    #create duration_tour and number_of_tour table from main table
    curser.execute('CREATE TABLE  duration_tour AS SELECT name,sum(duration) as durations  FROM main GROUP BY name;') 
    curser.execute('CREATE TABLE IF NOT EXISTS number_of_tour AS SELECT name,sum(number) as numbers  FROM main GROUP BY name;') 

    #create a csv file from main table
    with open('web/report/report.csv', mode='w',encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        tour_list=read_from_datebase('main','tour_date')
        
        writer.writerow(['ردیف','نام','تاریخ','مدت به دقیقه','تعداد'])
        for i in tour_list:
            writer.writerow(i)

    #create a csv file from duration_tour table
    with open('web/report/report_duration_tour.csv', mode='w',encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        tour_list=read_from_datebase('duration_tour','durations')
        writer.writerow(['نام','مدت'])
        for i in tour_list:
            writer.writerow(i)
        


    #create a csv file from number_of_tour table
    with open('web/report/report_number_of_tour.csv', mode='w',encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        tour_list=read_from_datebase('number_of_tour','numbers')
        writer.writerow(['نام','تعداد'])
        for i in tour_list:
            writer.writerow(i)

    name=''
    date=''
    left=[]
    height=[]


    with open('web/report/report_duration_tour.csv',encoding="utf_8") as f:
        csv_reader = csv.reader(f, delimiter=',')

        line_count = 0
        

        for row in csv_reader:
            if line_count > 0 and line_count%2 == 0:
            # if line_count > 0 :

                
                name=row[0]
                print(name)
                name=similar(name)
                print(name)

                
                data=float(row[1])
                left.append(name)
                height.append(data)
            line_count+=1
    print('%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%')
    print(left)
    print(height)
    return (left,height)



def read_data():

    #create and connect to report_datebase

    conn=sqlite3.connect('web/report/report_database')
    curser=conn.cursor()


    #function for reading a table from date base and return data of row in list of list
    def read_from_datebase(table_name,order):
        _list=[]
      
        curser.execute('SELECT * FROM %s ORDER BY %s ' %(table_name,order))
        rows=curser.fetchall()
        for row in rows:
            row=list(row)
            _list.append(row)
        return _list


    tour_list=read_from_datebase('main','tour_date')
        
    return tour_list
        
  
