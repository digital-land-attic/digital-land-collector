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
            items.append(item.metadata)

    print("PUBLICATIONS=", end='')
    for publication in publications:
        print("\\\n   %s" % (path), end='')
    print("\n")

    print("FEATURES=", end='')
    for item in items:
        if 'feature' not in item:
            item['feature'] = os.path.join('data/feature', item['publication'] + '.geojson')
        print("\\\n   %s" % (item['feature']), end='')
    print("")

    for item in items:
        if (item['task'] in ['geojson']):
            if 'cache' not in item:
                item['cache'] = os.path.join('cache/', item['publication'] + '.' + item['task'])
            print("""
{cache}:
\t@mkdir -p cache
\tcurl --silent --show-error '{data-url}' > $@

{feature}:\t{cache}
\t@mkdir -p data/feature
\togr2ogr -f geojson -t_srs EPSG:4326 '$@' '{cache}'

""".format(**item))
