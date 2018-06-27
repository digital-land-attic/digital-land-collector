#!/usr/bin/env python3

"""
    simplify geojson output by ogr2ogr GeoJSON driver
    - limits coordinates to 6 decimal places

    Assumes coordinates are in WGS84
"""
import sys

try:
    import ijson.backends.yajl2_cffi as ijson
    input = sys.stdin.buffer
except ImportError:
    import ijson
    input = sys.stdin

output = sys.stdout

import json
import os
from decimal import Decimal
import hashlib


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



def feature(f, item, publication, prefix, key):
    if f['type'] != 'Feature':
        raise ValueError('invald feature', f['type'])

    p = f['properties']


    properties = {}

    properties['item'] = item

    if publication:
        properties['publication'] = publication

    if key and key in p:
        properties['feature'] = "%s:%s" % (prefix, p[key])

    # collect properties from source data
    properties['source_properties'] = p

    return {
        "type": "Feature",
        "properties": properties,
        "geometry": geometry(f['geometry'])
    }


def dumps(obj):
    return json.dumps(obj, default=decimal_default, separators=(',', ':'), sort_keys=True)


def c14n(publication, prefix, key, ifp=input, ofp=output):
    print('{ "type": "FeatureCollection", "features": [', file=ofp, end="")

    features = ijson.items(ifp, 'features.item')
    try:
        while True:
            f = next(features)
            if 'geometry' in f and f['geometry']:
                item = hashlib.md5(dumps(f).encode('utf-8')).hexdigest()
                print(dumps(feature(f, item, publication, prefix, key)), file=ofp, end="")
                print(',', end="")
    except StopIteration:
        try:
            if 'geometry' in f and f['geometry']:
                item = hashlib.md5(dumps(f).encode('utf-8')).hexdigest()
                print(dumps(feature(f, item, publication, prefix, key)), file=ofp, end="")
        except UnboundLocalError:
            pass

    print(']}', file=ofp, end="")


if __name__ == "__main__":
    c14n(publication=sys.argv[1], prefix=sys.argv[2], key=sys.argv[3])
