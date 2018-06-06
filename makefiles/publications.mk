PUBLICATIONS=\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md

FEATURES=\
   data/feature/lambeth-wards.geojson\
   data/feature/local-authority-districts.geojson\
   data/feature/national-park-boundary.geojson

var/cache/lambeth-wards.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'https://opendata.arcgis.com/datasets/473a6365b6e54fe98b56229dd40eb79e_1.geojson' > $@



var/cache/local-authority-districts.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'https://opendata.arcgis.com/datasets/fab4feab211c4899b602ecfbfbc420a3_1.geojson' > $@



var/cache/national-park-boundary.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'http://geoportal1-ons.opendata.arcgis.com/datasets/df607d4ffa124cdca8317e3e63d45d78_1.geojson' > $@


