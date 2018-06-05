import json
import sys
import os
import requests
from decimal import Decimal
from pyproj import Proj, transform

projection = {
    'bng': Proj(init='EPSG:27700'),
    'wgs84': Proj(init='EPSG:4326')
}


def c14n(geojson, geography, key):

    def coordinates(c):

        return [round(Decimal(c[0]), 5), round(Decimal(c[1]), 5)]

    def point(g):
        return {
            "type": "Point",
            "coordinates": coordinates(g['coordinates'])
        }

    def polygon(g):
        return {
            "type": "Polygon",
            "coordinates": [[coordinates(c) for c in l] for l in g['coordinates']]
        }

    def multipolygon(g):
        return {
            "type": "MultiPolygon",
            "coordinates": [[[coordinates(c) for c in l] for l in ll] for ll in g['coordinates']]
        }


    def geometry(g):
        if g['type'] == 'Point':
            return point(g)
        elif g['type'] == 'Polygon':
            return polygon(g)
        elif g['type'] == 'MultiPolygon':
            return multipolygon(g)
        else:
            raise ValueError('invald geometry', g['type'])

    def properties(p):
        return {
            'area': "%s:%s" % (geography, p[key])
        }

    def feature(f):
        if f['type'] != 'Feature':
            raise ValueError('invald feature', f['type'])

        return {
            "type": "Feature",
            "properties": properties(f['properties']),
            "geometry": geometry(f['geometry'])
        }

    def collection(c):
        if c['type'] != 'FeatureCollection':
            raise ValueError('invalid geojson')

        return {
            "type": "FeatureCollection",
            "features": [feature(f) for f in geojson['features']]
        }

    return collection(geojson)


def dump(geojson, output):
    json.dump(geojson, output, default=decimal_default, separators=(',', ':'))


def load(i):
    return json.load(i)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


if __name__ == "__main__":
    r = requests.get(sys.argv[1])
    geojson = r.json()
    geojson = c14n(geojson, sys.argv[2], sys.argv[3])
    dump(geojson, sys.stdout)
