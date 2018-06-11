PUBLICATIONS=\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md\
   data/publication/national-park-boundary.md

FEATURES=\
   data/feature/green-belt.geojson\
   data/feature/historic-landfill.geojson\
   data/feature/lambeth-wards.geojson\
   data/feature/local-authority-districts.geojson\
   data/feature/mayoral-development-corporation-boundary.geojson\
   data/feature/national-park-boundary.geojson

var/cache/green-belt.zip:
	@mkdir -p var/cache
	curl --silent --show-error 'http://maps.communities.gov.uk/geoserver/dclg_inspire/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=dclg_inspire:Local_Authority_Greenbelt_boundaries_2016-17&outputFormat=shape-zip&srsName=EPSG:4326' > $@


data/feature/green-belt.geojson:	var/cache/green-belt.zip
	@mkdir -p data/feature
	ogr2ogr -f geojson -t_srs EPSG:4326 $@ /vsizip/var/cache/green-belt.zip/Local_Authority_Greenbelt_boundaries_2016-17.shp


var/cache/historic-landfill.gml:
	@mkdir -p var/cache
	curl --silent --show-error 'http://www.geostore.com/OGC/OGCInterface;jsessionid=JJ7Qf4H4jNTPSzkZ3NXRe95s?SESSIONID=-2109512248&INTERFACE=ENVIRONMENTWFS&SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=ms:ea_wfs_historic_landfill' > $@


var/cache/lambeth-wards.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'https://opendata.arcgis.com/datasets/473a6365b6e54fe98b56229dd40eb79e_1.geojson' > $@


var/cache/local-authority-districts.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'https://opendata.arcgis.com/datasets/fab4feab211c4899b602ecfbfbc420a3_1.geojson' > $@


var/cache/mayoral-development-corporation-boundary.zip:
	@mkdir -p var/cache
	curl --silent --show-error 'https://files.datapress.com/london/dataset/mayoral-development-corporation-boundary/mdc-boundary-post-consultation-shp.zip' > $@


data/feature/mayoral-development-corporation-boundary.geojson:	var/cache/mayoral-development-corporation-boundary.zip
	@mkdir -p data/feature
	ogr2ogr -f geojson -t_srs EPSG:4326 $@ /vsizip/var/cache/mayoral-development-corporation-boundary.zip/mdc-boundary-post-consultation.shp


var/cache/national-park-boundary.geojson:
	@mkdir -p var/cache
	curl --silent --show-error 'http://geoportal1-ons.opendata.arcgis.com/datasets/df607d4ffa124cdca8317e3e63d45d78_1.geojson' > $@

