import folium
from Grid import Region
import pandas as pd
from grid_visualize import get_index_high_ratio_24h

GRID_CONGESTED_THREASHOLD = 0.3


base_map = folium.Map(location=(42.30, -71.05), zoom_start=13)
congested_indexes = get_index_high_ratio_24h(GRID_CONGESTED_THREASHOLD)
reg = Region(42.70, -71.50, 42.10, -70.75)
reg.add_ratio()

for label in congested_indexes:
	grid = reg.find_grid(label)


	grid_center = ((grid.x + grid.m) / 2, (grid.y + grid.n) / 2)
	folium.Marker(grid_center, icon=folium.Icon(color='blue')).add_to(base_map)

grids = [reg.find_grid(label) for label in congested_indexes]
maxi_g = max(grids, key=lambda x: x.congestion_ratio)
maxi_center = ((maxi_g.x + maxi_g.m) / 2, (maxi_g.y + maxi_g.n) / 2)
folium.Marker(maxi_center, popup='most congested', icon=folium.Icon(color='red')).add_to(base_map)

base_map.save('q1.html')

