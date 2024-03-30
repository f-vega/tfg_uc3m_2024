import os

def dividir_por_sector(input_folder, output_folder):
    # Crear las carpetas de salida si no existen
    for sector in ['primario', 'secundario', 'terciario']:
        sector_folder = os.path.join(output_folder, sector)
        if not os.path.exists(sector_folder):
            os.makedirs(sector_folder)

    # Obtener la lista de archivos CSV en la carpeta de entrada
    archivos_csv = [archivo for archivo in os.listdir(input_folder) if archivo.endswith('.csv')]

    # Mapear cada archivo a su sector correspondiente
    for archivo in archivos_csv:
        if 'agricultura' in archivo or 'ganaderia' in archivo or 'pesca' in archivo:
            sector = 'primario'
        elif 'industria' in archivo or 'construccion' in archivo or 'electricidad' in archivo or 'agua' in archivo or 'metalurgia' in archivo:
            sector = 'secundario'
        else:
            sector = 'terciario'

        # Mover el archivo a la carpeta correspondiente
        archivo_path = os.path.join(input_folder, archivo)
        nuevo_path = os.path.join(output_folder, sector, archivo)
        os.replace(archivo_path, nuevo_path)

# Rutas de las carpetas de entrada y salida
input_folder = "./clean_data"
output_folder = "./dividido_por_sector"

# Dividir los archivos CSV por sector
dividir_por_sector(input_folder, output_folder)
