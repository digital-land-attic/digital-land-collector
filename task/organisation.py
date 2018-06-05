import os
import csv
import luigi
import requests
from register import Records


class Organisation(luigi.Task):

    def run(self):
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

        with self.output().open("w") as output:
            r.dump(file=output, 
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

    def output(self):
        return luigi.LocalTarget("data/organisation.tsv")
