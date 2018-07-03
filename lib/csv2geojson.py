#!/usr/bin/env python3

import sys
import csv
import pyproj
import geojson


bng = pyproj.Proj(init='epsg:27700')
wgs84 = pyproj.Proj(init='epsg:4326')


def geometry(row):
    lon = float(row['GeoX'])
    lat = float(row['GeoY'])

    if lon > 10000:
        # sniffed bng coordinate system
        lon, lat = pyproj.transform(bng, wgs84, lon, lat)
    elif lon > 49 and lon < 60 and lat < 0:
        # sniffed swapped coordinates
        lat, lon = lon, lat

    return {
        "type": "Point",
        "coordinates": [lon, lat]
    }


def feature(row):
    return {
        "type": "Feature",
        "properties": row,
        "geometry": geometry(row)
    }


class items(object):
    def __init__(self, fp):
        self.reader = csv.DictReader(fp)
   
    def __iter__(self):
        return self
   
    def __next__(self):
        return feature(next(self.reader))


def csv2geojson(input=sys.stdin, file=sys.stdout):
    geojson.c14n(items(input), file=file)


if __name__ == "__main__":
    csv2geojson()
