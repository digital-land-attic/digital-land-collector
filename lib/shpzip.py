#!/usr/bin/env python


"""
Convert a shape file to c14n geojson
"""

import zipfile
from io import BytesIO
import sys
import shapefile
from pyproj import Proj, transform

bng = Proj(init='epsg:27700')
wgs84 = Proj(init='EPSG:4326')

zipshape = zipfile.ZipFile(sys.stdin, 'rb'))

names = zipshape.namelist()

shpname = next(n for n in names if n.endswith('.shp'))
name = shpname[:-4]

reader = shapefile.Reader(
    shp=BytesIO(zipshape.read(name + '.shp')),
    shx=BytesIO(zipshape.read(name + '.shx')),
    dbf=BytesIO(zipshape.read(name + '.dbf')))

fields = reader.fields[1:]
field_names = [field[0] for field in fields]

buffer = []
for s in reader.shapeRecords():
    geometry = s.shape.__geo_interface__
    #lon, lat = transform(bng, wgs84, *geometry['coordinates'])

    r = dict(zip(field_names, s.record))

    item = {
        'dataset': 'listed-building',
        'listed-building': r['ListEntry'],
        'name': r['Name'],
        'listed-building-grade': r['Grade'],
        'start-date': "{:%Y-%m-%d}".format(r['ListDate']),
    }
    if (r.get('AmendDate', None)):
        item['entry-date'] = "{:%Y-%m-%d}".format(r['AmendDate'])

    properties = { 'listed-building': item['listed-building'] }
    feature = dict(type="Feature", geometry=geometry, properties=properties)
    buffer.append(feature)


if __name__ == "__main__":
