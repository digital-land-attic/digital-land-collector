#!/usr/bin/env python3

import json
import sys
import os
from decimal import Decimal
from pyproj import Proj, transform

projection = {
    'bng': Proj(init='EPSG:27700'),
    'wgs84': Proj(init='EPSG:4326')
}

count = 0

def c14n(geojson, prefix, key):

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
        global count
        if key and key in p:
            f="%s:%s" % (prefix, p[key])
        else:
            f=count
            count = count + 1
        return { 'feature': f }

    def feature(f):

        print(f)

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
            "features": [feature(f) for f in c['features'] if f.get('geometry') is not None]
        }

    return collection(geojson)


def dump(geojson, output):
    json.dump(geojson, output, default=decimal_default, separators=(',', ':'), sort_keys=True)


def load(i):
    return json.load(i)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


if __name__ == "__main__":
    geojson = load(sys.stdin)
    geojson = c14n(geojson, prefix=sys.argv[1], key=sys.argv[2])
    dump(geojson, sys.stdout)
