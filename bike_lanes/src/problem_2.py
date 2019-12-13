import csv
import matplotlib.pyplot as plt
index = 0
neighbors = {}
with open('bike_block.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[20]!=' ' and row[20]!='neighborhood' and row[20] not in neighbors.keys():
            neighbors[row[20]] = 1
        elif row[20] in neighbors.keys():
            neighbors[row[20]]+=1

print(neighbors)

result_neighbor_key = []
result_neighbor_value = []
for i in neighbors.values():
    result_neighbor_value.append(i)
for i in neighbors.keys():
    result_neighbor_key.append(i)
print(result_neighbor_key)
#plt.bar(range(len(neighbors)),result_neighbor_value,tick_label = range(len(neighbors)))
#plt.show()
