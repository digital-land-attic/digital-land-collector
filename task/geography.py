import os
import luigi
import requests
import frontmatter
import geojson
import csv
import json


class Geography(luigi.WrapperTask):
    def requires(self):
        for row in csv.DictReader(open('data/publication/index.tsv'), delimiter='\t'):
            path = os.path.join('data/publication', row['path'])
            if path.endswith('.md'):
                item = frontmatter.load(path)
                task = item['task']
                if (task in ['geojson']):
                    publication = item['publication']
                    prefix = item['prefix']
                    url = item['data-url']
                    key = item['key']

                    yield GeoJSON(publication, prefix, url, key)
                    
                    if item.get('fields', None):
                        yield Data(publication, prefix, url, key, item['fields'], item['properties'])


class GeoJSON(luigi.Task):
    publication = luigi.Parameter()
    prefix = luigi.Parameter()
    url = luigi.Parameter()
    key = luigi.Parameter()

    def run(self):
        print("+ fetching", self.url)
        r = requests.get(self.url, allow_redirects=True)
        g = geojson.c14n(r.json(), self.prefix, self.key)

        with self.output().open("w") as output:
            geojson.dump(g, output)

    def output(self):
        return luigi.LocalTarget("data/area/{0}.geojson".format(self.publication))


class Data(luigi.Task):
    """
    Extract data from geojson
    """
    publication = luigi.Parameter()
    prefix = luigi.Parameter()
    url = luigi.Parameter()
    key = luigi.Parameter()
    fields = luigi.Parameter()
    properties = luigi.Parameter()

    def run(self):
        print("+ fetching", self.url)
        r = requests.get(self.url, allow_redirects=True)

        with self.output().open("w") as output:
            sep = '\t'
            fields = ['area'] + [s.strip() for s in self.fields.split(',')]
            properties = ['area'] + [s.strip() for s in self.properties.split(',')]
            print(sep.join(fields), file=output)
            for f in r.json()['features']:
                p = f['properties']
                p['area'] = "%s:%s" % (self.prefix, p[self.key])
                print(sep.join([p[field].strip() if p.get(field) is not None else '' for field in properties]), file=output)

    def output(self):
        return luigi.LocalTarget("data/data/{0}.tsv".format(self.publication))
