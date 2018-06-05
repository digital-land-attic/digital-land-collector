.SUFFIXES:
.SUFFIXES: .zip .gml .geojson
.PRECIOUS: cache/%.zip data/feature/%.geojson
.SECONDARY: cache/%.zip data/feature/%.geojson
.PHONY: init makefiles clobber clean prune
.DELETE_ON_ERROR:

all: makefiles targets

-include makefiles/publications.mk

TARGETS=\
	$(FEATURES)\
	data/organisation.tsv

#makefiles/publications.mk:

targets:	$(TARGETS)

data/organisation.tsv:	etc/development-corporation.tsv etc/national-park.tsv lib/organisation.py
	@mkdir -p data
	python3 lib/organisation.py > $@

init::
	pip3 install -r requirements.txt

makefiles: makefiles/publications.mk

clobber::
	rm -f $(TARGETS)

clean::
	rm -rf cache

prune::	clean
	rm -f .cache.sqlite
