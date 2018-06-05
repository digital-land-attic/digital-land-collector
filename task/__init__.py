import luigi
import requests_cache
from .organisation import Organisation
from .geography import Geography

requests_cache.install_cache('.cache')


class DigitalLand(luigi.WrapperTask):

    def requires(self):
        yield Organisation()
        yield Geography()

    def run(self):
        print("+ DigitalLand")
