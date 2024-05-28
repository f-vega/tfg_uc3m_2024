import geopandas as gpd

# Ruta al archivo SHP extraído
shp_file_path = 'openlayers/geo_data/DIVISIONES_ADMINISTRATIVAS_CM.gpkg'

# Leer el archivo SHP
gdf = gpd.read_file(shp_file_path)
gdf = gdf.to_crs('EPSG:4326')

# Convertir a GeoJSON
geojson_path = 'delimiter.geojson'
gdf.to_file(geojson_path, driver='GeoJSON')

