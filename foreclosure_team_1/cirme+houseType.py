from folium import plugins
import folium
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generateBaseMap(default_location=[42.3601, -71.0589]):
    base_map = folium.Map(location=default_location ) 
    return base_map

# crime

crimedata = pd.read_csv('crime.csv')
crimedata.dropna()

crimedata=crimedata.dropna(subset=['Long'])
crimedata=crimedata.dropna(subset=['Lat'])

base_map = generateBaseMap()
plugins.HeatMap(data=crimedata[['Lat', 'Long']], radius=8, max_zoom=13).add_to(base_map)
base_map.save('crime.html')

id_list = ['Larceny','Property Lost','Residential Burglary','Robbery','Vandalism','Disorderly Conduct','Commercial Burglary']
crimedata = crimedata[crimedata['OFFENSE_CODE_GROUP'].isin(id_list)]

crimedata['OFFENSE_CODE_GROUP'].value_counts().plot(kind='barh',alpha=0.7,figsize=(6,6))
plt.show()

foreclosureData = pd.read_excel('Foreclosure_Data.xlsx')

forclosure_map = generateBaseMap()
plugins.HeatMap(data=foreclosureData[['Parcel: Y Coordinate', 'Parcel: X Coordinate']], radius=8, max_zoom=13).add_to(forclosure_map)
forclosure_map.save('foreclosure.html')

m = generateBaseMap()
plugins.HeatMap(data=crimedata[['Lat', 'Long']], radius=8, max_zoom=13).add_to(m)
plugins.HeatMap(data=foreclosureData[['Parcel: Y Coordinate', 'Parcel: X Coordinate']], radius=8,gradient={1:'green'}, max_zoom=13).add_to(m)

m.save('m.html')

# type of house

housetype = pd.read_excel('Foreclosure_Data.xlsx')
housetype['Occupancy Description (fm Prcl)'].value_counts().plot(kind='barh',alpha=0.7,figsize=(10,10))
plt.show()

data = housetype['Occupancy Description (fm Prcl)'].value_counts()

Single_family = ["SINGLE FAM DWELLING"]

Two_family = ["TWO-FAM DWELLING"]
Three_family = ["THREE-FAM DWELLING"]

Commercial= [ "ELEC SUBSTATION",  "STORAGE WHSE (OLD)", "COMM MULTI-USE", "RET/WHSL/SERVICE", "MACHINE SHOP (SMALL)", "REPAIR GARAGE", "STRIP RETAIL/ OFFICE", "WAREHOUSE /DISTRIB", "OLD MANUFACTURING", "RETAIL STORE DETACHED", "LAUNDRY OPERATION", "RESTAURANT/CAFETERIA", "INDUSTRIAL LOFT", "RESTAURANT/LOUNGE", "FAST FOOD RESTAURANT", "COMMERCIAL LAND", "LAUNDROMAT /CLEANER", "NIGHT CLUB", "WHSE: INDUSTRIAL", "AUDITORIUM /THEATER", "MOVIE THEATER", "SUPERMARKET", "COM LAND (UNUSABLE)"]

Health_Care= [ "HOSPITAL (EXEMPT)", "NURSING/CONV HOME", "MEDICAL OFFICE"]

Educational_Recreational= ["SOCIAL CLUB", "CLASSROOM", "DAY CARE CENTER", "TRAINING /PRIV EDUC"]

Other_Government= ["U.S. GOVERNMENT", "OTHER PUBLIC LAND", "BOST REDEVELOP AUTH", "SUBSD HOUSING S- 8", "BOST HOUSING AUTHORITY"]

Religious =  [ "CHURCH, SYNAGOGUE", "RELIGIOUS ORGANIZATION"]

Other_Residential_Buildings = [ "OTHER EXEMPT BLDG", "APT 4-6 UNITS", "CONDO MAIN", "APT 7-30 UNITS", "MULTIPLE BLDGS/1 LOT", "APT 31-99 UNITS"]

Undecidable= ["RES /COMMERCIAL USE"]
    
titles = ["Single_family", "Commercial", "Two_family", "Three_family", "Other_Residential_Buildings", "Undecidable", "Other_Government",
          "Educational_Recreational", "Religious", "Health_Care"
                ]
values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for index,row in data.items():    
    if index in Single_family:
        values[0] = values[0] + row
    if index in Commercial:
        values[1] = values[1] + row
    if index in Two_family:
        values[2] = values[2] + row
    if index in Three_family:
        values[3] = values[3] + row
    if index in Other_Residential_Buildings:
        values[4] = values[4] + row        
    if index in Undecidable:
        values[5] = values[5] + row
            
    if index in Other_Government:
        values[6] = values[6] + row
    if index in Educational_Recreational:
        values[7] = values[7] + row
    if index in Religious:
        values[8] = values[8] + row
    if index in Health_Care:
        values[9] = values[9] + row
    
index = np.arange(10)
width = 0.45
    
color=["#87CEFA", "#008B8B", "#2E8B57", "#C0FF3E", "#FFEC8B", 
        "#FFC125", "#8B658B", "#FF6A6A", "#FF1493", "#1C1C1C", "#9A32CD", "#828282", "#F0FFF0"]
    
plt.figure(figsize=(20, 10))
plt.bar(index, values, width, label="num", color=[color[0]])

    
plt.xlabel('category')
plt.ylabel('number')
plt.title('Statistics for foreclosure categories')
plt.xticks(index, titles)

plt.savefig('houseType.jpg')
plt.show()