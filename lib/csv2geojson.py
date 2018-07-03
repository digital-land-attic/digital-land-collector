#!/usr/bin/env python3

import sys
import csv
import pyproj
import geojson


bng = pyproj.Proj(init='epsg:27700')
wgs84 = pyproj.Proj(init='epsg:4326')


def geometry(row):
    try:
        lon = float(row['GeoX'])
        lat = float(row['GeoY'])
        if lon > 10000:
            # sniffed bng coordinate system
            lon, lat = pyproj.transform(bng, wgs84, lon, lat)
        elif lon > 49 and lon < 60 and lat < 0:
            # sniffed swapped coordinates
            lat, lon = lon, lat
    except Exception as e:
        print("invalid point:", row, file=sys.stderr)
        raise e

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


def items(fp):
    for row in csv.DictReader(fp):
        if all(not(value) for value in row.values()):
            # some CSV files contain blank lines
            continue

        if row.get('GeoY') == 'GeoY':
            # some CSV files contain duplicate title rows
            continue

        yield feature(row)


def csv2geojson(input=sys.stdin, file=sys.stdout):
    geojson.c14n(items(input), file=file)


if __name__ == "__main__":
    csv2geojson()
