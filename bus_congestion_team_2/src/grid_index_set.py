import folium
import Grid as grid
import googlemaps
from datetime import datetime
import numpy as np
import polyline


def getIndexSet(A, B, visited):
    A = A if A[0] <= B[0] else B
    if A[0] <= B[0] and A[1] >= B[1]:
        # top left --> bottom right
        dir = -1
    else:
        # bottom left --> top right
        dir = 1
    region = grid.Region(42.70, -71.50, 42.10, -70.75)
    region.add_ratio()

    delta = 0.005
    indexSet = set()
    ratioList = []
    x = A[0]
    y = A[1]
    while x <= B[0]:
        index = region.locate((x, y))
        if index not in visited:
            visited.add(index)
            g = region.find_grid(index)
            ratio = g.congestion_ratio
            ratioList.append(ratio)
            indexSet.add(tuple([index, ratio]))
            x += delta
            y += dir*delta
            if (dir>0 and y > B[1]) or (dir<0 and y < B[1]):
                break
        else:
            x += delta
            y += dir * delta
            if (dir > 0 and y > B[1]) or (dir < 0 and y < B[1]):
                break
    return indexSet, ratioList, visited


def scoring(route):
    scores = list()
    visited = set()
    for i in range(len(route) - 1):
        indexList, score, visited = getIndexSet(route[i], route[i+1], visited)
        scores += score
    return np.mean(scores)


def draw_map(points):
    start_coords = (42.351293, -71.105243)
    folium_map = folium.Map(location=start_coords,
                            zoom_start=10,
                            control_scale=True,
                            tiles='Stamen Toner')
    for i in range(len(points)):
        folium.CircleMarker((points[i][0], points[i][1]),
                            radius=6,
                            color='#FFB6C1',
                            fill_color='#FFB6C1',
                            ).add_to(folium_map)
    route = folium.PolyLine(points,
                            weight=5,
                            color='green',
                            opacity=1
                            ).add_to(folium_map)
    folium_map.save('rec_route.html')


def get_rec_route(start, end, ori_score):
    with open('../csv/GoogleAPIKey.txt', 'r') as f:
        API_key = f.readline()
    gmaps = googlemaps.Client(key=API_key)
    now = datetime.now()
    directions_result = gmaps.directions(start,
                                         end,
                                         departure_time=now,
                                         alternatives=True)
    routes = []
    points = set()
    route_score = {}
    encoded_route = {}

    # get all alternative routes
    for i in directions_result:
        routes.append(i['legs'][0]['steps'])

    # use the first alternative route to test the score-process
    for route in routes:
        points = []
        encoded_points = []
        points.append(tuple(start))
        for i in route:
            points.append(tuple([i['end_location']['lat'], i['end_location']['lng']]))
            encoded_points.append(i['polyline']['points'])
        mean_ratio = scoring(points)
        route_score[tuple(points)] = mean_ratio
        encoded_route[tuple(points)] = encoded_points
    min_score = min(route_score.values())
    if min_score < ori_score:
        map_points = []
        rec_route = [key for key, score in route_score.items() if score == min_score]
        rec_route = encoded_route[rec_route[0]]
        for i in rec_route:
            map_points += polyline.decode(i)
        # print(map_points)
        return True, map_points
    else:
        return False, [start, end]

if __name__=='__main__':
    points = []
    map_points = []
    A = (42.350714, -71.105378)
    B = (42.336303, -71.168433)
    score = 0.5
    flag, map_points = get_rec_route(A, B, score)
    draw_map(map_points)
    