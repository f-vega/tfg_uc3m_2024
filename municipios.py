import json, csv

# Nombre del archivo GeoJSON
archivo_geojson = "./openlayers/geo_data/municipios.geojson"
# Nombre del archivo CSV
archivo_csv = "dataset.csv"

# Lista para almacenar las filas coincidentes
filas_coincidentes = []

# Cargar los datos del archivo CSV en un diccionario
municipios_madrid = set()

with open(archivo_csv, "r", encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    next(reader)
    for row in reader:
        municipios_madrid.add(row[2])


# Leer el archivo GeoJSON
with open(archivo_geojson, "r", encoding='utf-8') as geojson_file:
    data = json.load(geojson_file)
    for feature in data["features"]:
        municipio = feature["properties"]["NAMEUNIT"]
        pre= municipio.split(' ')[0]
        post= ' '.join(municipio.split(' ')[1:])
        if 'El' in pre or 'La' in pre or 'Los' in pre or 'Las' in pre:
            municipio = f'{post} ({pre})'
        if municipio in municipios_madrid:
            filas_coincidentes.append(feature)

# Guardar las filas coincidentes en un nuevo archivo GeoJSON
nuevo_archivo_geojson = "openlayers/geo_data/municipios.geojson"
with open(nuevo_archivo_geojson, "w") as geojson_file:
    json.dump({"type": "FeatureCollection", "features": filas_coincidentes}, geojson_file)
