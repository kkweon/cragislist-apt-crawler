import numpy as np
import pandas as pd

from craigslist_apt import geocoding
from craigslist_apt import settings


class CalTrain:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = float(lat)
        self.lon = float(lon)

    def __str__(self):
        return "[{}, {}, {}]".format(self.name, self.lat, self.lon)

    def get_distance(self, lat, lon):
        R = 6371e3

        lat = float(lat)
        lon = float(lon)

        lon_diff = np.deg2rad(lon - self.lon)
        lat = np.deg2rad(lat)
        lon = np.deg2rad(lon)

        lat2 = np.deg2rad(self.lat)
        lon2 = np.deg2rad(self.lon)

        # d = acos( sin φ1 ⋅ sin φ2 + cos φ1 ⋅ cos φ2 ⋅ cos Δλ ) ⋅ R
        # var φ1 = lat1.toRadians(), φ2 = lat2.toRadians(), Δλ = (lon2-lon1).toRadians(), R = 6371e3;
        # ACOS( SIN(lat1)*SIN(lat2) + COS(lat1)*COS(lat2)*COS(lon2-lon1) ) * 6371000
        a = np.sin(lat) * np.sin(lat2) + np.cos(lat) * np.cos(lat2) * np.cos(lon_diff)
        return np.arccos(a) * R / 1000 * 0.621371


def get_distance_from_work(lat, lon):
    R = 6371e3
    lon = float(lon)
    lat = float(lat)

    work_lat = settings.WORK_LAT
    work_lon = settings.WORK_LON

    lon_diff = np.deg2rad(lon - work_lon)
    lat = np.deg2rad(lat)
    lon = np.deg2rad(lon)

    lat2 = np.deg2rad(work_lat)
    lon2 = np.deg2rad(work_lon)

    a = np.sin(lat) * np.sin(lat2) + np.cos(lat) * np.cos(lat2) * np.cos(lon_diff)
    return np.arccos(a) * R / 1000 * 0.621371

def read_data(data_file=None):
    if data_file is None:
        data = pd.read_csv(settings.CALTRAIN_DATA)
    else:
        data = pd.read_csv(data_file)
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

def get_closest_caltrain_by_lat_lon(caltrain_stops, lat, lon):
    result = geocoding.get_address_by_lat_lon(lat, lon)
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
        min_dist = 10000000000
        station = None

        for cal_stop in caltrain_stops:
            dist = cal_stop.get_distance(lat, lon)
            if dist < min_dist:
                station = cal_stop
                min_dist = dist

        return "", station.name, min_dist


if __name__ == "__main__":
    caltrain_data = read_data("../data/stops.txt")

    #test_address = "3800 north el mirage rd"
    # test_address = "372 Euclid, Cashion, OK 73016, USA"
    test_lat = 37.711100
    test_lon = -122.413744
    # test_lat = 37.776984
    # test_lon = -122.393836

    print(get_distance_from_work(test_lat, test_lon))
