PUBLICATIONS=\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md

FEATURES=\
   data/feature/local-authority-districts.geojson\
   data/feature/national-park-boundary.geojson

var/cache/local-authority-districts.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'https://opendata.arcgis.com/datasets/fab4feab211c4899b602ecfbfbc420a3_1.geojson' > $@

data/feature/local-authority-districts.geojson:	var/cache/local-authority-districts.geojson
	@mkdir -p data/feature
	ogr2ogr -f geojson -t_srs EPSG:4326 '$@' 'var/cache/local-authority-districts.geojson'



var/cache/national-park-boundary.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'http://geoportal1-ons.opendata.arcgis.com/datasets/df607d4ffa124cdca8317e3e63d45d78_1.geojson' > $@

data/feature/national-park-boundary.geojson:	var/cache/national-park-boundary.geojson
	@mkdir -p data/feature
	ogr2ogr -f geojson -t_srs EPSG:4326 '$@' 'var/cache/national-park-boundary.geojson'


