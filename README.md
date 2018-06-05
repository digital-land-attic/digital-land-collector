# Digital land data

Configuration and tools to collect geographical data published by government which may be useful for people building houses.

    * [data/publication](publication) — source publications
    * [data/licence](licence) — licence terms and conditions
    * [data/copyright](copyright) — copyright, attribution terms and conditions
    * [etc](etc) — prototype register data

# Collected data

Data is collected and transformed into a consistent format in the [data/feature](data/feature) directories.

These files are large, so are published in the following repositories:

    * [digital-land-data](https://github.com/communitiesuk/digital-land-data) 
    * [landregistry-index-data](https://github.com/communitiesuk/landregistry-index-data)

You can explore the data using the [digital-land-explorer](https://github.com/communitiesuk/digital-land-explorer) application.

# Building the data

The datasets are collected using download and conversion scripts in the [bin](bin) and [lib](lib) directories.

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python dependencies:

    $ make init

# Adding a publication

To add a publication, add a line to a file in the [publication](publication) directory, then re-build the makefiles:

    $ make makefiles

# Collecting data

The process of refreshing the data is being automated as a pipeline of tasks:

    $ make

# Licence

The software in this project is open source and covered by LICENSE file.

Individual datasets copied into this repository may have specific copyright and licensing, otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
