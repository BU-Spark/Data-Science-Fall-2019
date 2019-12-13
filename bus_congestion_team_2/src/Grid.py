import os
import pickle


def get_grid_congestion_ratio():
    # get number of different time slots for calculation
    count = 0
    for file in os.listdir("../bot/output/"):
        count += 1

    with open('grid_congestion.data', 'rb') as handle:
        all_grid_congestion_dict = pickle.load(handle)

    all_grid_congestion_dict /= count
    all_grid_congestion_dict /= max(all_grid_congestion_dict)  # normalize the data

    return all_grid_congestion_dict


def get_grid_congestion_ratio_24h():
    with open('grid_congestion_24h.data', 'rb') as handle:
        all_grid_congestion_dict = pickle.load(handle)

    all_grid_congestion_dict /= 14  # the total number of days collected
    all_grid_congestion_dict /= max(all_grid_congestion_dict)  # normalize the data

    return all_grid_congestion_dict


def float_range(start, stop, step):
    neg = False if step > 0 else True

    if neg:
        start, stop = -start, -stop
        step = -step

    while start < stop:
        yield start if not neg else -start
        start += step


class Grid(object):
    # inputs:
    # @x : top-left latitude
    # @y : top-left longitude
    # @m : bottom-right latitude
    # @n : bottom-right longitude
    def __init__(self, label, x, y, m, n):
        self.label = label
        self.x = x
        self.y = y
        self.m = m
        self.n = n
        self.congestion_ratio = None

    def has(self, pt_x, pt_y):
        if pt_x <= self.x and pt_x >= self.m and pt_y <= self.n and pt_y >= self.y:
            return True

        return False

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.m == other.m and self.n == other.n: return True
        return False

    def __repr__(self):
        return f'<#{self.label} Grid: {self.m} < x < {self.x} and {self.y} < y < {self.n}>, #ratio={self.congestion_ratio}'


class Region(object):
    def __init__(self, top_left_latitude, top_left_longitude, bottom_right_latitude, bottom_right_longitude,
                 cell_width=0.001, cell_height=0.001):
        self.grids = dict()  # key - value:
        self.cell_width = cell_width
        self.cell_height = cell_height

        self.tl_lati = top_left_latitude
        self.tl_long = top_left_longitude
        self.br_lati = bottom_right_latitude
        self.br_long = bottom_right_longitude

        index = 0
        lat_range = list(float_range(top_left_latitude, bottom_right_latitude, -cell_height))
        lon_range = list(float_range(top_left_longitude, bottom_right_longitude, cell_width))

        self.height = len(lat_range)
        self.width = len(lon_range)

        for lat in lat_range:
            for lon in lon_range:
                tlx, tly = lat, lon
                brx, bry = lat - cell_height, lon + cell_width
                self.grids[index] = Grid(index, tlx, tly, brx, bry)
                index += 1

    def locate(self, pnt):
        x, y = pnt
        index = self._quick_index(x, y)
        upper_bound = self.width * self.height

        if index < 0 or index >= upper_bound:
            print(f'ERR: returned label#{index} out of bound, label should be within [0, {upper_bound})')
            return -1

        return index

    def find_grid(self, label):
        upper_bound = self.width * self.height
        if label < 0 or label >= upper_bound:
            print(f'ERR: label#{label} out of bound, label should be within [0, {upper_bound})')
            return None

        return self.grids.get(label, None)

    def add_ratio(self):

        ratios = get_grid_congestion_ratio()
        for i in range(len(ratios)):
            self.grids[i].congestion_ratio = ratios[i]

    def _quick_index(self, x, y):
        delta_lon = (y - self.tl_long) / self.cell_width
        delta_lati = (x - self.tl_lati) / -self.cell_height

        return int(delta_lati) * self.width + int(delta_lon)


if __name__ == '__main__':
    region = Region(42.70, -71.50, 42.10, -70.75)
    region.add_ratio()
    loc = (42.34728891, -71.03881597)
    # loc = (42.70, -71.50)

    # The label would be an integer like 0, 1, 2, ... to indicate a specific Grid object
    # You're able to get that Grid by calling find_grid with pass the label returned by locate()
    label = region.locate(loc)
    g = region.find_grid(label)
    print(g)
    print(g.congestion_ratio)
