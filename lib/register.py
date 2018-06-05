#!/usr/bin/env python3

import os
import sys
import io
import csv
import requests
from natsort import natsorted


class Records():
    """
    Register client
    """

    url = 'https://%s.register.gov.uk/records.tsv?page-index=%d&page-size=%d'
    delimiter = '\t'

    def __init__(self):
        self.records = {}
        self.fields = set(['record'])

    def map(self, record, row, map):
        row['record'] = record
        for f in map:
            if callable(map[f]):
                row[f] = map[f](row)
            else:
                row[f] = row.get(map[f], row.get(f, ''))
        return row

    def rows(self, map={}):
        for record in natsorted(self.records):
            row = self.records[record].copy()
            row = self.map(record, row, map)
            yield row

    def record(self, register, row):
        return '%s:%s' % (register, row[register])

    def put(self, register, row, map={}):
        self.records[self.record(register, row)] = row
        self.fields = self.fields.union(set(row.keys()))

    def load_local(self, register, path=None, map={}):
        if not path:
            path = os.path.join('etc', register + '.tsv')
        for row in csv.DictReader(open(path), delimiter=self.delimiter):
            self.put(register, row, map)

    def load(self, register, url=None, page_index=1, page_size=5000, map={}):
        if url is None:
            url = self.url

        while True:
            resp = requests.get(url=url % (register, page_index, page_size))
            resp.raise_for_status()

            count = 0
            for row in csv.DictReader(io.StringIO(resp.text), delimiter=self.delimiter):
                self.put(register, row, map)
                count += 1

            if count < page_size:
                break
            page_index += 1

    def dump(self, fields=None, map={}, key=None, sep='\t', file=sys.stdout):
        if fields is None:
            fields = self.fields
            fields = natsorted(list(fields))

        print(sep.join(fields), file=file)

        for row in self.rows(map=map):
            print(sep.join([str(row.get(field, '')) for field in fields]), file=file)


if __name__ == "__main__":
    r = Records()
    for register in sys.argv[1:]:
        r.load(register)
    r.dump()
