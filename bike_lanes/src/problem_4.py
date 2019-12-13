import csv
import matplotlib.pyplot as plt
date = []
years = {}
months = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
month_name = ['January','February','March','April','May','June','July','August','September','October',
              'November','December']
neighbors = []
with open('bike_block.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[1]!='' and row[1]!='open_dt':
            day = row[1].split()
            date.append(day[0])
            temp = day[0].split('-')
            year = temp[0]
            month = int(temp[1])-1
            dayreal = temp[2]
            if year not in years.keys():
                years[year] = [1,0]
            else:
                years[year][0]+=1
            months[month][0]+=1
            if row[4] == 'ONTIME':
                years[year][1]+=1
                months[month][1]+=1
year_ratio = []
month_ratio = []
for i in years.keys():
    print(i+':'+'{} bike lane block occuers, solving ontime ratio is {:.2%}'.format(years[i][0],years[i][1]/
                                                                  years[i][0]))
    year_ratio.append(years[i][1]/years[i][0])
for i in range(len(months)):
    print('In '+month_name[i]+', {} bike lane block occuers, solving ontime ratio is {:.2%}'.format(months[i][0],
                                                                        months[i][1]/months[i][0]))
    month_ratio.append(months[i][1]/months[i][0])
#print(years)
#print(months)
month_result = []
for i in months:
    month_result.append(i[0])
result_year_key = []
result_year_value = []
for i in years.values():
    result_year_value.append(i[0])
for i in years.keys():
    result_year_key.append(i)

plt.bar(range(12),month_ratio,tick_label = month_name)
plt.show()
