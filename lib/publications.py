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

                publication = item['publication'].replace(':', '-')

                item['cache'] = item.get('cache', os.path.join('var/cache/', publication + item['suffix']))
                item['feature'] = item.get('feature', os.path.join('data/feature', publication + '.geojson'))

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
""".format(**item))
        if item['task'] == 'shape-zip':
            print("""
{feature}:\t{cache}
\t@mkdir -p data/feature
\togr2ogr -f geojson -t_srs EPSG:4326 $@ /vsizip/{cache}/{shape-zip-path}
""".format(**item))
