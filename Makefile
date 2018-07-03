.SUFFIXES:
.SUFFIXES: .zip .gml .geojson .kml
.PHONY: init makefiles publications targets clobber clean prune
.SECONDARY:
.DELETE_ON_ERROR:

all: makefiles etc publications targets

#
#  make dependencies
#
INDEXES=\
	data/publication/index.tsv

MAKEFILES=\
	makefiles/publications.mk

-include makefiles/publications.mk

makefiles/publications.mk:	$(INDEXES) $(PUBLICATIONS) data/publication/index.tsv lib/publications.py
	@mkdir -p makefiles
	python3 lib/publications.py < data/publication/index.tsv > $@

#
#  targets
#
TARGETS=\
	data/organisation.tsv \
	data/publication/index.tsv \
	$(FEATURES)

ETC=\
	etc/development-corporation.tsv\
	etc/company.tsv\
	etc/national-park.tsv

data/organisation.tsv:	$(ETC) lib/organisation.py
	@mkdir -p data
	python3 lib/organisation.py > $@

#
#  convert to geojson with WGS84 coordinates
#
var/geojson/%.geojson: var/cache/%.geojson
	@mkdir -p var/geojson/
	ogr2ogr -f geojson -t_srs EPSG:4326 $@ $<

var/geojson/%.geojson: var/cache/%.gml
	@mkdir -p var/geojson/
	ogr2ogr -f geojson -t_srs EPSG:4326 $@ $<

var/geojson/%.geojson: var/cache/%.kml
	@mkdir -p var/geojson/
	ogr2ogr -f geojson -t_srs EPSG:4326 $@ $<

#
#  convert spreadsheets to CSV
#
var/csv/%.csv: var/cache/%.txt
	@mkdir -p var/csv/
	iconv -f ISO8859-1 -t UTF-8 $< > $@

var/csv/%.csv: var/cache/%.csv
	@mkdir -p var/csv/
	in2csv $< > $@

var/csv/%.csv: var/cache/%.xls
	@mkdir -p var/csv/
	in2csv $< > $@

var/csv/%.csv: var/cache/%.xlsx
	@mkdir -p var/csv/
	in2csv $< > $@

#
#  rebuild publication index
#
data/publication/index.tsv:
	bin/index.sh data/publication > $@

#
#  phony
#
makefiles:: $(MAKEFILES)
indexes:: $(INDEXES)
publications::	$(PUBLICATIONS)
targets::	$(TARGETS)
etc::	$(ETC)

init::
	pip3 install -r requirements.txt

clobber::
	rm -f $(TARGETS)

clean::
	rm -f $(MAKEFILES) $(INDEXES)

prune::	clean clobber
	rm -rf var
