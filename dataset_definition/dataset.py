import os, csv, json

def dataset(input_path, output_path):
    # Crear un diccionario para almacenar los datos unidos
    join_data = {}

    # Obtener la lista de archivos en la carpeta
    folders = os.listdir(input_path)
    folders = sorted(folders, key=lambda x: x != 'zonas_estadisticas')
    for folder in folders:
        folder_path = os.path.join(input_path, folder)
        files = os.listdir(folder_path)
        for file in files:
            if file.endswith('.csv'):
                with open(os.path.join(folder_path, file), 'r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    headers = next(csv_reader)
                    file_name = file[:-4]

                    # Iterar sobre cada fila en el archivo CSV
                    for row in csv_reader:
                        serie = row[0] if row else ""
                        codigo_municipio = row[1] if len(row) > 1 else ""
                        nombre = row[2] if len(row) > 2 else ""
                        
                        # Verificar si la serie, código de municipio y nombre ya están en el diccionario
                        if (serie, codigo_municipio, nombre) not in join_data:
                            join_data[(serie, codigo_municipio, nombre)] = {}
                        
                        file_path = os.path.join(folder_path, file)

                        if 'municipio_comunidad_madrid' in file_path or 'parcelas' in file_path:
                            for i in range(3, 7):
                                file_name = headers[i]
                                join_data[(serie, codigo_municipio, nombre)][file_name] = row[i]
                                
                        elif 'poblacion_censada_2020' in file_path:
                            file_name = headers[3]
                            join_data[(serie, codigo_municipio, nombre)][file_name] = row[3]
                                
                        elif 'pib_2020' in file_path:
                            join_data[(serie, codigo_municipio, nombre)][file_name] = row[-1]

                        else:
                            join_data[(serie, codigo_municipio, nombre)][file_name] = row[3]

    # Escribir los datos unidos en un nuevo archivo CSV
    with open(output_path, 'w', newline='', encoding='ISO-8859-1') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')

        final_keys = []
        for key, values in join_data.items():
            if final_keys == []:
                final_keys.extend(values.keys())
        final_keys = [str(key) for key in final_keys]

        # Escribir los encabezados en el archivo CSV
        csv_writer.writerow(['Serie', 'Codigo_municipio', 'Nombre', *final_keys])

        # Escribir los datos sumados
        for key, values in join_data.items():
            line = [key[0], key[1], key[2]]
            for clave in final_keys:
                line.append(values.get(clave, ''))
            csv_writer.writerow(line)

    