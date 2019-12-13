import pandas as pd

data = pd.read_csv("filtered_data_1.csv")
print("=============================")

result1 = data.groupby('owner_name').sum()['sqm_imperv'].sort_values(ascending=False) * 0.000247105381
print(result1)
clean_data = data[data['sqm_bldg'] > 0]
print("=============================")

result2 = clean_data.groupby('owner_name').sum()['sqm_imperv'].sort_values(ascending=False) * 0.000247105381
print(result2)
clean_data = clean_data[clean_data['numBusStops_25']!=-1]

candidates = clean_data[(clean_data['avgDistanceBusStops'] < 1) |
                        (clean_data['avgDistanceSubwayStops'] < 1) |
                        (clean_data['avgDistanceTrainStops'] < 1)]
print("=============================")

result3 = candidates.groupby('owner_name').sum()['sqm_imperv'].sort_values(ascending=False) * 0.000247105381
print(result3)

