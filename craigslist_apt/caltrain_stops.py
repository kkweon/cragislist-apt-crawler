import numpy as np
import pandas as pd
import settings


class CalTrain:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "[{}, {}, {}]".format(self.name, self.lat, self.lon)

    def get_distance(self, lat, lon):
        lat_diff = lat - self.lat
        lon_diff = lon - self.lon

        return np.sqrt(lat_diff ** 2 + lon_diff ** 2)


def read_data():
    data = pd.read_csv(settings.CALTRAIN_DATA)
    caltrain_stops = set()
    for idx, row in data.iterrows():
        caltrain = CalTrain(row['stop_name'], row['stop_lat'], row['stop_lon'])
        caltrain_stops.add(caltrain)

    return caltrain_stops


if __name__ == "__main__":
    data = read_data()
    for i in data:
        print(i.get_distance(0, 0))
