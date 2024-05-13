import os
from clean import clean_folder, sector_sum

# EJEMPLO
input_folder = './original_data'

for folder_name in os.listdir(input_folder):
    # Combinar el nombre del directorio con la ruta base para obtener la ruta completa
    folder_path = os.path.join(input_folder, folder_name)
        # Tiene un encoding diferent

    # Verificar si el elemento es un directorio
    if os.path.isdir(folder_path):
        # Aquí puedes hacer lo que necesites con el directorio
        output_path = clean_folder(folder_path)
        output_path_2020 = clean_folder(folder_path, 2020)
        if 'sector' in folder_path:
            keywords= output_path.split('/')[-1][:-7]
            sector_sum(keyword=keywords, folder=output_path)

