import numpy as np
import pandas as pd

from craigslist_apt import geocoding
from craigslist_apt import settings

class CalTrain:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "[{}, {}, {}]".format(self.name, self.lat, self.lon)

    def get_distance(self, lat, lon):
        R = 6371e3

        lon_diff = np.deg2rad(lon - self.lon)
        lat = np.deg2rad(lat)
        lon = np.deg2rad(lon)

        lat2 = np.deg2rad(self.lat)
        lon2 = np.deg2rad(self.lon)

        # d = acos( sin φ1 ⋅ sin φ2 + cos φ1 ⋅ cos φ2 ⋅ cos Δλ ) ⋅ R
        # var φ1 = lat1.toRadians(), φ2 = lat2.toRadians(), Δλ = (lon2-lon1).toRadians(), R = 6371e3;
        # ACOS( SIN(lat1)*SIN(lat2) + COS(lat1)*COS(lat2)*COS(lon2-lon1) ) * 6371000
        a = np.sin(lat) * np.sin(lat2) + np.cos(lat) * np.cos(lat2) * np.cos(lon_diff)
        return np.arccos(a) * R / 1000


def read_data():
    data = pd.read_csv(settings.CALTRAIN_DATA)
    caltrain_stops = set()
    for idx, row in data.iterrows():
        caltrain = CalTrain(row['stop_name'], row['stop_lat'], row['stop_lon'])
        caltrain_stops.add(caltrain)

    return caltrain_stops


def get_closest_caltrain(caltrain_stops, address):
    result = geocoding.get_lat_lon(address)

    if result is not None:
        formal_name, lat, lon = result
        min_dist = 10000000000
        station = None


        for cal_stop in caltrain_stops:
            dist = cal_stop.get_distance(lat, lon)
            if dist < min_dist:
                station = cal_stop
                min_dist = dist

        return formal_name, station.name, min_dist

    else:
        return address, "", ""



if __name__ == "__main__":
    caltrain_data = read_data()

    test_address = "1429 sunnydale ave"

    print(get_closest_caltrain(caltrain_data, test_address))
