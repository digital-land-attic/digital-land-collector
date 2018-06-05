#!/usr/bin/env python3

import sys
import requests
import requests_cache
import shutil

requests_cache.install_cache('.cache')


def fetch(url, fp):
    response = requests.get(url, stream=True, allow_redirects=True)
    shutil.copyfileobj(response.raw, fp)
    del response


if __name__ == "__main__":
    fetch(sys.argv[1], sys.stdout.buffer)
