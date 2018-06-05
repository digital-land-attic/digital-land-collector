PUBLICATIONS=\
   data/publication/national-park-boundary.md

FEATURES=\
   data/feature/national-park-boundary.geojson

cache/national-park-boundary.geojson:
	@mkdir -p cache
	curl --silent --show-error 'http://geoportal1-ons.opendata.arcgis.com/datasets/df607d4ffa124cdca8317e3e63d45d78_1.geojson' > $@

data/feature/national-park-boundary.geojson:	cache/national-park-boundary.geojson
	@mkdir -p data/feature
	ogr2ogr -f geojson -t_srs EPSG:4326 '$@' 'cache/national-park-boundary.geojson'


