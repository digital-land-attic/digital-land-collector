.SUFFIXES:
.SUFFIXES: .zip .gml .geojson .kml
.PHONY: init makefiles publications targets clobber clean prune
.SECONDARY:
.DELETE_ON_ERROR:

all: makefiles etc publications targets

#
#  make dependencies
#
MAKEFILES=\
	makefiles/publications.mk

-include makefiles/publications.mk

makefiles/publications.mk:	$(PUBLICATIONS) data/publication/index.tsv lib/publications.py
	@mkdir -p makefiles
	python3 lib/publications.py < data/publication/index.tsv > $@

#
#  targets
#
TARGETS=\
	data/organisation.tsv \
	$(FEATURES)

ETC=\
	etc/development-corporation.tsv\
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
	ogr2ogr -f geojson -s_srs EPSG:27700 -t_srs EPSG:4326 $@ $<

var/geojson/%.geojson: var/cache/%.kml
	@mkdir -p var/geojson/
	ogr2ogr -f geojson -t_srs EPSG:4326 $@ $<


#
#  phony
#
makefiles:: $(MAKEFILES)
publications::	$(PUBLICATIONS)
targets::	$(TARGETS)
etc::	$(ETC)

init::
	pip3 install -r requirements.txt

clobber::
	rm -f $(TARGETS)

clean::
	rm -f $(MAKEFILES)

prune::	clean clobber
	rm -rf var
