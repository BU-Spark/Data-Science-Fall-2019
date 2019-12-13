import folium
import pandas as pd
import numpy as np

pathBPS = '../rawData/bps.csv'
path_save = '../csv/BPSfilted.csv'
col = ('logtime', 'latitude', 'longitude', 'speed', 'vendorhardwareid')

def generateBaseMap(points1, points2):
    default_location = [42.3, -71]
    base_map = folium.Map(location=default_location)
    for points in (points1, points2):
        while points:
            point = points.pop()
            la = point[0]
            lo = point[1]
            dir = str(la) + ', ' + str(lo)
            folium.CircleMarker((la, lo),
                                radius=3,
                                color='#00BFFF',
                                fill_color='#00BFFF',
                                popup=dir
                                ).add_to(base_map)

    base_map.save('BPSBoundary.html')


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
    if max(listla) < maxLa and min(listla) > minLa and max(listlo) < maxLo and min(listlo) > minLo:
        ind1 = np.argmax(listla)
        ind2 = np.argmin(listla)
        ind3 = np.argmax(listlo)
        ind4 = np.argmin(listlo)
        maxPoints.append([listla[ind1], listlo[ind1]])
        maxPoints.append([listla[ind3], listlo[ind3]])
        minPoints.append([listla[ind4], listlo[ind4]])
        minPoints.append([listla[ind2], listlo[ind2]])
generateBaseMap(maxPoints, minPoints)
