#!/usr/bin/env python3

import os
import sys
import csv
import frontmatter

"""
Create makefile dependencies for publications
"""

delimiter = '\t'

if __name__ == "__main__":
    print("PUBLICATIONS=", end='')
    for row in csv.DictReader(sys.stdin, delimiter=delimiter):
        path = os.path.join('data/publication', row['path'])
        print("\\\n   %s" % (path), end='')
    print()
