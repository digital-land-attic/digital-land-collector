#!/usr/bin/env python3

"""
    simplify geojson output by ogr2ogr GeoJSON driver
    - limits coordinates to 6 decimal places

    Assumes coordinates are in WGS84
"""
import sys

try:
    import ijson.backends.yajl2_cffi as ijson
    stdin = sys.stdin.buffer
except ImportError:
    import ijson
    stdin = sys.stdin

import json
import os
from decimal import Decimal
import hashlib


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def coordinates(c):
    try:
        return [round(Decimal(c[0]), 5), round(Decimal(c[1]), 5)]
    except Exception as e:
        print("invalid coordinates:", c, file=sys.stderr)
        return [0, 0]


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

    f['properties']['item'] = item

    if publication:
        f['properties']['publication'] = publication

    if key and key in f['properties']:
        f['properties']['feature'] = "%s:%s" % (prefix, f['properties'][key])

    return {
        "type": "Feature",
        "properties": f['properties'],
        "geometry": geometry(f['geometry'])
    }


def dumps(obj):
    return json.dumps(obj, default=decimal_default, separators=(',', ':'), sort_keys=True)


def c14n(items, publication=None, prefix=None, key=None, file=sys.stdout):
    print('{ "type": "FeatureCollection", "features": [', file=file, end="")
    sep = ""

    for f in items:
        if 'geometry' in f and f['geometry']:
            item = hashlib.md5(dumps(f).encode('utf-8')).hexdigest()
            print(sep)
            print(dumps(feature(f, item, publication, prefix, key)), file=file, end="")
            sep = ","

    print(']}', file=file, end="")


if __name__ == "__main__":
    c14n(
        ijson.items(stdin, 'features.item'),
        publication=sys.argv[1],
        prefix=sys.argv[2],
        key=sys.argv[3])
