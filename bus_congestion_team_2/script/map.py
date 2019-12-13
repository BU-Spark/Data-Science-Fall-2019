import folium
import pandas as pd
import numpy as np

pathBPS = '../rawData/bps.csv'
path_save = '../csv/BPSfilted.csv'
col = ('logtime', 'latitude', 'longitude', 'speed', 'vendorhardwareid')

def generateBaseMap(points1, points2):
    default_location = [42.3, -71]
    base_map = folium.Map(location=default_location)
    while points1:
        point = points1.pop()
        la = point[0]
        lo = point[1]
        folium.CircleMarker((la, lo),
                            radius=1,
                            color='r',
                            fill_color='r',
                            ).add_to(base_map)
    while points2:
        point = points2.pop()
        la = point[0]
        lo = point[1]
        folium.CircleMarker((la, lo),
                            radius=1,
                            color='r',
                            fill_color='r',
                            ).add_to(base_map)
    base_map.save('test.html')


data = pd.read_csv(pathBPS, usecols=col, chunksize=10000)
i = 0
maxLa = 42.587435
maxLo = -70.845016
minLo = -71.291173
minLa = 42.106555
maxPoints, minPoints = [], []
for chunk in data:
    i += 1
    print(i)
    listla = chunk['latitude'].to_list()
    listlo = chunk['longitude'].to_list()
    print(max(listla) < maxLa and min(listla) > minLa and max(listlo) < maxLo and min(listlo) > minLo)
    if max(listla) < maxLa and min(listla) > minLa and max(listlo) < maxLo and min(listlo) > minLo:
        ind1 = np.argmax(listla)
        print(ind1)
        ind2 = np.argmin(listla)
        maxPoints.append([listla[ind1], listlo[ind1]])
        minPoints.append([listla[ind2], listlo[ind2]])
generateBaseMap(maxPoints, minPoints)