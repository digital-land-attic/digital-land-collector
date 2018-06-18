#!/usr/bin/env python3

"""
    simplify geojson output by ogr2ogr GeoJSON driver
    - limits coordinates to 6 decimal places

    Assumes coordinates are in WGS84
"""

try:
    import ijson.backends.yajl2_cffi as ijson
except ImportError:
    import ijson

import json
import sys
import os
from decimal import Decimal


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def coordinates(c):
    return [round(Decimal(c[0]), 5), round(Decimal(c[1]), 5)]


def point(g):
    return {
        "type": "Point",
        "coordinates": coordinates(g['coordinates'])
    }


def polygon(g):
    return {
        "type": "MultiPolygon",
        "coordinates": [[[coordinates(c) for c in l] for l in g['coordinates']]]
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


def properties(p, prefix, key):
    if key and key in p:
        f="%s:%s" % (prefix, p[key])
        return { 'feature': f }
    else:
        return {}


def feature(f, prefix, key):
    if f['type'] != 'Feature':
        raise ValueError('invald feature', f['type'])

    return {
        "type": "Feature",
        "properties": properties(f['properties'], prefix, key),
        "geometry": geometry(f['geometry'])
    }


def dump(obj, file):
    json.dump(obj, file, default=decimal_default, separators=(',', ':'), sort_keys=True)


def c14n(prefix, key, ifp=sys.stdin, ofp=sys.stdout):
    print('{ "type": "FeatureCollection", "features": [', file=ofp)

    features = ijson.items(ifp, 'features.item')
    for f in features:
        if 'geometry' in f and f['geometry']:
            dump(feature(f, prefix, key), file=ofp)
            print(file=ofp)

    print(']}', file=ofp)


if __name__ == "__main__":
    c14n(prefix=sys.argv[1], key=sys.argv[2])
