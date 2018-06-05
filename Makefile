.SUFFIXES:
.SUFFIXES: .zip .gml .geojson
.PRECIOUS: cache/%.zip data/feature/%.geojson
.SECONDARY: cache/%.zip data/feature/%.geojson
.PHONY: init makefiles clobber clean prune
.DELETE_ON_ERROR:

all: makefiles targets

-include makefiles/publications.mk
-include makefiles/features.mk

TARGETS=\
	$(FEATURES)\
	data/organisation.tsv

MAKEFILES=\
	makefiles/publications.mk\
	makefiles/features.mk


makefiles/publications.mk:	data/publication/index.tsv
	@mkdir -p makefiles
	python3 lib/publications.py < data/publication/index.tsv > $@

makefiles/features.mk:	data/publication/index.tsv $(PUBLICATIONS)
	@mkdir -p makefiles
	python3 lib/features.py < data/publication/index.tsv > $@


data/organisation.tsv:	etc/development-corporation.tsv etc/national-park.tsv lib/organisation.py
	@mkdir -p data
	python3 lib/organisation.py > $@


init::
	pip3 install -r requirements.txt

makefiles: $(MAKEFILES)

targets:	$(TARGETS)

clobber::
	rm -f $(TARGETS)

clean::
	rm -f $(MAKEFILES)

prune::	clean
	rm -rf cache
	rm -f .cache.sqlite
