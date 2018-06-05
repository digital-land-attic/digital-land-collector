.SUFFIXES:
.SUFFIXES: .zip .gml .geojson
.PRECIOUS: cache/%.zip data/feature/%.geojson
.SECONDARY: cache/%.zip data/feature/%.geojson
.PHONY: init makefiles clobber clean prune
.DELETE_ON_ERROR:

all: makefiles publications targets

MAKEFILES=\
	makefiles/publications.mk

-include makefiles/publications.mk

TARGETS=\
	data/organisation.tsv \
	$(FEATURES)

ETC=\
	etc/development-corporation.tsv\
	etc/national-park.tsv 

makefiles/publications.mk:	data/publication/index.tsv lib/publications.py
	@mkdir -p makefiles
	python3 lib/publications.py < data/publication/index.tsv > $@

data/organisation.tsv:	etc lib/organisation.py
	@mkdir -p data
	python3 lib/organisation.py > $@

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

prune::	clean
	rm -rf cache
	rm -f .cache.sqlite
