import os, csv

# Función clean para preprocesar los datos y eliminar las líneas sobrantes
def clean(input_path, output_path, unuseful_words = ['Serie'], selected_year = 2023):
    with open(input_path, 'r') as f_input:
        if f_input != '':
            next(f_input)
        clean_lines = []
        clean_lines.append(f'Serie;Codigo_municipio;Nombre;{selected_year}\n')
        delete_next = False
        for line in f_input:
            if not delete_next:
                delete = False
                for word in unuseful_words:
                    if word in line:
                        delete = True
                if line.strip() == '':
                    delete = True
                elif '(A)' in line:
                    line = line.replace('(A) Avance ;', '')
                if not delete:
                    fields = line.strip().split(';')
                    if selected_year==2020:
                        clean_lines.append(';'.join(fields[:3] + fields[-5:-4]) + '\n')
                    else:
                        clean_lines.append(';'.join(fields[:3] + fields[-2:]) + '\n')
                # Eliminar filas posteriores al último municipio
                if 'Zarzalejo' in line:
                        delete_next = True
    with open(output_path, 'w') as f_output:
         for line in clean_lines:
            f_output.write(line)

def clean_folder(input_path, selected_year=2023):

    if selected_year == 2020:
        output_path = f'./clean_data_2020/{os.path.basename(input_path)}'
    else:
        output_path = f'./clean_data/{os.path.basename(input_path)}'
    if not os.path.exists(output_path):
            os.makedirs(output_path)

    csv_files = [file for file in os.listdir(input_path) if file.endswith('.csv')]
    for file in csv_files:
        f_input_path = f'{input_path}/{file}'
        f_output_path = f'{output_path}/{file}'
        clean(f_input_path, f_output_path, selected_year=selected_year)

# EJEMPLO
input_folder = './original_data'

for folder_name in os.listdir(input_folder):
    # Combinar el nombre del directorio con la ruta base para obtener la ruta completa
    folder_path = os.path.join(input_folder, folder_name)
    
    # Verificar si el elemento es un directorio
    if os.path.isdir(folder_path):
        # Aquí puedes hacer lo que necesites con el directorio
        clean_folder(folder_path)
        clean_folder(folder_path, 2020)

# def refactor(example_file, input_file, output_file):


def sector_sum(keyword, folder):
    sector_data = {'primario': {}, 'secundario': {}, 'terciario': {}}
    primario_keywords = ['agricultura', 'ganaderia', 'pesca', 'primario']
    secundario_keywords = ['industria', 'construccion', 'electricidad', 'agua', 'metalurgia', 'secundario']
    headers = ''
    if not os.path.exists(folder):
        os.makedirs(folder)
    csv_files = os.listdir(folder)
    csv_files = [file for file in csv_files if file.endswith('.csv')]

    for file in csv_files:
        if any(keyword in file for keyword in primario_keywords):
            sector = 'primario'
        elif any(keyword in file for keyword in secundario_keywords):
            sector = 'secundario'
        else:
            sector = 'terciario'
        file_path = os.path.join(folder, file)

        with open(os.path.join(folder, file), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            headers = next(csv_reader)
            # Iterar sobre cada fila en el archivo CSV,
            for row in csv_reader:
                serie = row[0] if row else ''
                codigo_municipio = row[1] if len(row) > 1 else ''
                nombre = row[2] if len(row) > 2 else ''
            # Verificar si ya existe una entrada para esta serie y código de municipio
                key = (serie, codigo_municipio, nombre)
                if key in sector_data[sector]:
                    # Sumar los valores de cada año
                    sector_data[sector][key] += int(row[3]) if row[3] else 0
                else:
                    # Si no existe, crear una nueva entrada en el diccionario
                    sector_data[sector][key] = int(row[3]) if row[3] else 0

        os.remove(file_path)

    # Escribir los datos sumados por sector en archivos CSV
    for sector, datos_sumados in sector_data.items():
        output_path = os.path.join(folder, f'{keyword}_{sector}.csv')

        with open(output_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(headers)
            for key, value in datos_sumados.items():
                csv_writer.writerow([key[0], key[1], key[2], value])

sector_sum('empleo', './clean_data/empleo_sector')
sector_sum('empleo', './clean_data_2020/empleo_sector')
sector_sum('unidades_productivas', './clean_data/unidades_productivas')
sector_sum('unidades_productivas', './clean_data_2020/unidades_productivas')
sector_sum('paro', './clean_data/paro_sector')
sector_sum('paro', './clean_data_2020/paro_sector')

