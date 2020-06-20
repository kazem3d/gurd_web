import csv
from gurd import similar

name=''
date=''
left=[]
height=[]


with open('report/report_duration_tour.csv',encoding="utf_8") as f:
    csv_reader = csv.reader(f, delimiter=',')

    line_count = 0
    

    for row in csv_reader:
        if line_count > 0 and line_count%2 == 0:
            
            name=row[0]
            print(name)
            name=similar(name)
            print(name)

            name=name[::-1]
            data=float(row[1])
            left.append(name)
            height.append(data)
        line_count+=1
print(left)
print(height)

