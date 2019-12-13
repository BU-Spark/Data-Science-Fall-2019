import pandas as pd
import matplotlib.pyplot as plt

# This code is to solve problem 3, and gonna use Boston and Cambridge's 311 data.
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth',50)
pd.set_option('display.width', 500)

# Process Boston's 311 data
df_boston = pd.read_csv("bike_block.csv")
df_boston['type breakdown'] = 'Others'
df_boston['closure_reason'] = df_boston['case_title'] + ' ' + df_boston['closure_reason']
df_boston = df_boston[['open_dt','closed_dt','type breakdown','latitude','longitude','closure_reason']]
print(df_boston.shape)
print(df_boston.head())

# Process Cambridge's 311 data
df_cambridge = pd.read_csv("Commonwealth_Connect_Bike_Lane_Obstruction_Heat_Map.csv")
df_cambridge['type breakdown'] = 'Others'
df_cambridge['ticket_created_date_time'] = pd.to_datetime(df_cambridge['ticket_created_date_time'])
df_cambridge['ticket_last_updated_date_time'] = pd.to_datetime(df_cambridge['ticket_last_updated_date_time'])
df_cambridge = df_cambridge[['ticket_created_date_time','ticket_last_updated_date_time','type breakdown','lat','lng','issue_description']]
df_cambridge.columns = ['open_dt','closed_dt','type breakdown','latitude','longitude','closure_reason']
print(df_cambridge.shape)
print(df_cambridge.head())

# Combine the two 311 data together
df = df_boston.append(df_cambridge,ignore_index=True)
print(df.shape)
print(df[516:520])

# Use different keywords to breakdown the block reasons
car = ['car','vehicle','park','truck','SUV','bus','shuttle','mercedes','driver','delivery','taxi']
tree = ['tree','branch']
uber_lyft = ['uber','lyft']
garbage = ['garbage','glass','dump','Storage container','trash']
repair = ['repair','potholes','paint']
snow = ['snow']

for i in range(df.shape[0]):
    flag = 0
    description = str(df.loc[i, 'closure_reason']).lower()
    if description == 'nan':
        df.loc[i, 'type breakdown'] = 'Blank'
        continue
    for ii in snow:
        if ii.lower() in description:
            df.loc[i, 'type breakdown'] = 'Snow'
            flag = 1
            break
    if flag == 1:
        continue
    for ii in garbage:
        if ii.lower() in description:
            df.loc[i, 'type breakdown'] = 'Garbage'
            flag = 1
            break
    if flag == 1:
        continue
    for ii in repair:
        if ii.lower() in description:
            df.loc[i, 'type breakdown'] = 'Repair'
            flag = 1
            break
    if flag == 1:
        continue
    for ii in tree:
        if ii.lower() in description:
            df.loc[i, 'type breakdown'] = 'Tree'
            flag = 1
            break
    if flag == 1:
        continue
    for ii in uber_lyft:
        if ii.lower() in description:
            df.loc[i, 'type breakdown'] = 'uber/lyft'
            flag = 1
            break
    if flag == 1:
        continue
    for ii in car:
        if ii.lower() in description:
            df.loc[i, 'type breakdown'] = 'Illegal parking'
            flag = 1
            break
    if flag == 1:
        continue

title = df["type breakdown"]
print(df.describe())
print(df.shape)

# Store the data for future use
df.to_csv('Boston_Cambridge.csv',index = False)

print(title.unique())
title_dic = {}
data = []
classes = ['Snow','Repair','Garbage','uber/lyft','Tree','Blank','Others','Illegal parking']

for i in classes:
    title_dic[i] = 0

for i in title:
    if i in title_dic:
        title_dic[i] += 1
    else:
        title_dic[i] = 1

# Sort the reasons by number
sorted_dic = sorted(title_dic.items(), key=lambda item: item[1])
print(sorted_dic)
sorted_classes = []
for i in sorted_dic:
    sorted_classes.append(i[0])
    data.append(i[1])

# Make a plot
print(data)
plt.figure(figsize=(10,6))
plt.xlabel('Classes',fontsize=14)
plt.ylabel('Number',fontsize=14)
for a,b in zip(sorted_classes,data):
    plt.text(a, b+0.1, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)
plt.bar(sorted_classes, data,align='center', alpha=0.5)
plt.show()

