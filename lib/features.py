#!/usr/bin/env python3

import os
import sys
import csv
import frontmatter

"""
Create makefile dependencies for features from publication markdown files
"""

delimiter = '\t'

if __name__ == "__main__":
    for row in csv.DictReader(sys.stdin, delimiter=delimiter):
        path = os.path.join('data/publication', row['path'])
        if path.endswith('.md'):
            item = frontmatter.load(path)
            task = item['task']

            if (task in ['geojson']):
                print("""
cache/{publication}.geojson:
\t@mkdir -p cache
\tcurl --silent --show-error '{data-url}' > $@

""".format(**item.metadata))
