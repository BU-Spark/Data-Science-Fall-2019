import pandas as pd
import matplotlib.pyplot as plt
import folium
import numpy as np
def data_processing(filename):
    df = pd.read_csv(filename)
    return df

df = data_processing('foreclosure.csv')
df = df[df['Parcel: X Coordinate'] != 'Parcel: X Coordinate']
print(df.columns)
# print(df.Suppressed.value_counts())
# print(df['USPS - Vacant'].value_counts())
def draw_mutiple_plot():
    reasons = ['Suppressed',
              'USPS - Vacant',
              'USPS - Inactive Address',
              'ISD - Vacant',
              'ISD - Condemned',
              'Boarded, Missing/Broken Windows or Doors',
              'Building/Structural Issue',
              'Discolored/Damage Exterior Wall',
              'Litter, Trash, and Old Mail',
              'Overgrown or neglected vegetation',
              'The absence of window coverings',
              'Open Building Violations',
              'Open Code Enforcement Cases',
              'REO Property',
              'Tax Title/Taxes Owed',
              'Utility Shut-Offs']

    # plt.figure(figsize=(30,10))
    # for i in range(1,17):
    #     plt.subplot(4,4,i)
    #     pd.value_counts(df[reasons[i-1]]).plot.bar(x=reasons[i-1], y='num', rot=0)
    # plt.show()

    cnt = []
    for i in range(len(reasons)):
        num = np.sum((df[reasons[i]]) == '1')
        print(reasons[i] + ' [numbers]: ', num)
        cnt.append(num)

    fg1 = plt.figure()
    plt.bar(reasons, cnt)
    plt.xticks(reasons,reasons, rotation='vertical')
    fg1.autofmt_xdate()
    plt.title('number of properties for each foreclosure reason')

    df[reasons] = df[reasons].replace('0', np.nan)
    zeros_list = df[reasons].isnull().sum(axis=1).tolist()
    cnt = 0
    for num in zeros_list:
        if num == 16:
            cnt = cnt + 1
    print(cnt)
    ones_list = [ 16 - x for x in zeros_list]
    df['number of reasons'] = ones_list
    df_reason = []
    for i in range(17):
        df_reason.append(np.sum(df['number of reasons'] == i))

    fg2 = plt.figure()
    x = np.arange(17)
    plt.bar(x, df_reason)
    plt.xticks(x,x)
    fg2.autofmt_xdate()
    plt.title('number of properties for breaking multiple rules')


    fg3 = plt.figure()
    print(df['Parcel: BPDA Neighborhood'].value_counts())
    pd.value_counts(df['Parcel: BPDA Neighborhood']).plot.bar()
    fg3.autofmt_xdate()
    plt.show()

def generateBaseMap(default_location = [42.3601, -71.0589], default_zoom_start=12):
    base_map = folium .Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map


def draw_map(data, colors):
    base_map = generateBaseMap()
    for index, row in data.iterrows():
        if row['Petitioned in Last 5 Years ']  == 'X' or row['Deed in Last 5 Years ']  == 'X':
            folium.CircleMarker(location=[row['Parcel: Y Coordinate'], row['Parcel: X Coordinate']], radius=2, color = colors[1]).add_to(base_map)
        else:
            folium.CircleMarker(location=[row['Parcel: Y Coordinate'], row['Parcel: X Coordinate']], radius=2, color = colors[0]).add_to(base_map)
    base_map.save('point_map.html')

colors = ['green', 'red']
draw_map(df, colors)