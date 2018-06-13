#!/usr/bin/env python3

import os
import sys
import csv
import frontmatter

"""
Create makefile dependencies for features from publication markdown files
"""

delimiter = '\t'
publications = []
items = []

if __name__ == "__main__":
    for row in csv.DictReader(sys.stdin, delimiter=delimiter):
        path = os.path.join('data/publication', row['path'])
        publications.append(path)

        if path.endswith('.md'):
            item = frontmatter.load(path)
            if (item['task'] in ['geojson', 'gml', 'kml', 'shape-zip']):

                if item['task'] == 'shape-zip':
                    suffix = '.zip'
                else:
                    suffix = '.' + item['task']

                item['suffix'] = item.get('suffix', suffix)
                item['prefix'] = item.get('prefix', item['publication'])
                item['key'] = item.get('key', '')

                item['cache'] = item.get('cache', os.path.join('var/cache/', item['publication'] + item['suffix']))
                item['geojson'] = item.get('geojson', os.path.join('var/geojson', item['publication'] + '.geojson'))
                item['feature'] = item.get('feature', os.path.join('data/feature', item['publication'] + '.geojson'))

                items.append(item.metadata)

    # probably could be a jina or other template
    print("PUBLICATIONS=", end='')
    for publication in publications:
        print("\\\n   %s" % (publication), end='')
    print("\n")

    print("FEATURES=", end='')
    for item in items:
        print("\\\n   %s" % (item['feature']), end='')
    print("")

    for item in items:
        print("""
{cache}:
\t@mkdir -p var/cache
\tcurl --silent --show-error '{data-url}' > $@

{feature}:\t{geojson} lib/geojson.py
\t@mkdir -p data/feature
\tpython3 lib/geojson.py '{prefix}' '{key}' < {geojson} > $@
""".format(**item))

        if item['task'] == 'shape-zip':
            print("""
{geojson}:\t{cache}
\t@mkdir -p var/geojson
\togr2ogr -f geojson -t_srs EPSG:4326 $@ /vsizip/{cache}/{shape-zip-path}
""".format(**item))
