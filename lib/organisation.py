#!/usr/bin/env python3

import os
import csv
import requests
from register import Records


if __name__ == "__main__":
    r = Records()
    r.load('government-organisation')
    r.load('local-authority-eng')

    r.load_local('national-park')
    r.load_local('development-corporation')

    gss = Records()
    for register in [
        'statistical-geography-county-eng',
        'statistical-geography-unitary-authority-eng',
        'statistical-geography-london-borough-eng',
        'statistical-geography-metropolitan-district-eng',
        'statistical-geography-non-metropolitan-district-eng']:
        gss.load(register)

    for row in gss.rows():
        organisation = 'local-authority-eng:' + row['local-authority-eng']
        if organisation in r.records:
            r.records[organisation]['area'] = 'statistical-geography:' + row['key']

    r.dump(
        fields=[
            'organisation', 
            'name',
            'category',
            'website',
            'area',
            'start-date',
            'end-date'
        ],
        map={
            'organisation': 'record',
            'name': 'official-name',
            'category': lambda r: 'local-authority-type:' + r['local-authority-type'] if 'local-authority-type' in r else ''
        })
