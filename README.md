# Digital land data collector

Configuration and tools to collect geographical data published by government which may be useful for people building houses.

Data is collected and transformed into a consistent format in the data/feature and data/entry directories,
to be published in the following repositories:

  * [digital-land-data](https://github.com/communitiesuk/digital-land-data) 
  * [landregistry-index-data](https://github.com/communitiesuk/landregistry-index-data)

You can explore the data using the [digital-land-explorer](https://github.com/communitiesuk/digital-land-explorer) application.

<a href="https://www.flickr.com/photos/psd/42622352081/" title="digital-land"><img src="https://farm2.staticflickr.com/1744/42622352081_70e90a4622_b.jpg" width="1024" height="688" alt="digital-land"></a>

# Configuration

  * [data/publication](data/publication) — source publications
  * [data/licence](data/licence) — licence terms and conditions
  * [data/copyright](data/copyright) — copyright, attribution terms and conditions
  * [data/organisation](data/organisation.tsv) — publishing organisations

The [etc](etc) directory contains prototype register data where no [GOV.UK register](https://www.registers.service.gov.uk/) exists yet.

# Adding a publication

To add a publication, add a markdown file in the [publication](publication) directory with the following front matter fields:

| Field | Value | Example |
| :---- | :---- | :------ |
| `publication` | A unique, symbolic name for the publication | `national-park-boundaries` |
| `name` | A descriptive name for the publication | `National Park Boundary` |
| `organisation` | [organisation](data/organisation.tsv) reference | `government-organisation:D303` |
| `copyright` | [copyright](data/copyright) reference | `ons-boundary` |
| `licence` | [licence](data/licence) reference | `ogl` |
| `data-gov-uk` | [data.gov.uk](https://data.gov.uk) reference | `671bdd94-f9e8-41fd-997c-c371fca050de` |
| `documentation-url` | Link to documentation | `http://geoportal.statistics.gov.uk/datasets/national-parks-august-2016-full-extent-boundaries-in-great-britain` |
| `data-url` | Link to data | `http://geoportal1-ons.opendata.arcgis.com/datasets/df607d4ffa124cdca8317e3e63d45d78_1.geojson` |
| `task` | The collection task | `geojson` |
| `prefix` | A unique, symbolic name for the scope of identifiers | `national-park-boundary` |
| `key` | The property name to be taken as the identifier | `npark16cd` |

The markdown can contain information about the publication.

Add the path to your markdown file to the [publication index](data/publication/index.tsv) and rebuild the makefiles (below).

# Collecting data

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python dependencies:

    $ make init

Adding a file changes the dependencies. Ensure the new file path is in the [index.tsv](data/publication/index.tsv) file and rebuild the makefiles:

    $ make makefiles

The datasets are collected using download and conversion scripts in the [bin](bin) and [lib](lib) directories:

    $ make

# Licence

The software in this project is open source and covered by LICENSE file.

Individual datasets copied into this repository may have specific copyright and licensing, otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
