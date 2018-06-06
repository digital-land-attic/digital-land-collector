PUBLICATIONS=\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md

FEATURES=\
   data/feature/historic-landfill.geojson\
   data/feature/lambeth-wards.geojson\
   data/feature/local-authority-districts.geojson\
   data/feature/national-park-boundary.geojson

var/cache/historic-landfill.gml:
	@mkdir -p var/cache
	curl --silent --show-error 'http://www.geostore.com/OGC/OGCInterface;jsessionid=JJ7Qf4H4jNTPSzkZ3NXRe95s?SESSIONID=-2109512248&INTERFACE=ENVIRONMENTWFS&SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=ms:ea_wfs_historic_landfill' > $@



var/cache/lambeth-wards.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'https://opendata.arcgis.com/datasets/473a6365b6e54fe98b56229dd40eb79e_1.geojson' > $@



var/cache/local-authority-districts.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'https://opendata.arcgis.com/datasets/fab4feab211c4899b602ecfbfbc420a3_1.geojson' > $@



var/cache/national-park-boundary.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'http://geoportal1-ons.opendata.arcgis.com/datasets/df607d4ffa124cdca8317e3e63d45d78_1.geojson' > $@


