#!/usr/bin/env python3

import os
import glob
import sys
import csv
import frontmatter

delimiter = '\t'

fields = ['brownfield-site-publication', 'organisation', 'documentation-url', 'data-url', 'data-gov-uk', 'start-date', 'end-date']

n = 0
print(delimiter.join(fields))

if __name__ == "__main__":
    for path in glob.glob('data/publication/brownfield-sites/*.md'):
        n = n + 1
        item = frontmatter.load(path).metadata
        item['brownfield-site-publication'] = str(n)
        print(delimiter.join([item.get(field) or '' for field in fields]))
