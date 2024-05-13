import os, csv, random
from encoding import detect_encoding, convert_encoding, xls_to_csv

# Función clean para preprocesar los datos y eliminar las líneas sobrantes
def clean(input_path, output_path, unuseful_words = ['Serie'], selected_year = 2023, start = 3, end=0, exception=0):
    with open(input_path, 'r') as f_input:
        if f_input != '':
            next(f_input)
        clean_lines = []
        clean_lines.append(f'Serie;Codigo_municipio;Nombre;{selected_year}\n')
        delete_next = False
        for line in f_input:
            fields = line.strip().split(';')
            if not delete_next:
                delete = False
                for word in unuseful_words:
                    if word in line:
                        delete = True
                if line.strip() == '':
                    delete = True
                if all(field == '' for field in fields):
                    delete = True
                elif '(A)' in line:
                    line = line.replace('(A) Avance ;', '')
                    fields = line.strip().split(';')
                elif '-' in line and not delete_next:
                    if any('-' in field for field in fields[3:]):
                        fields = [field.replace('-', '0') for field in fields]
                if not delete:
                        if exception != 0:
                            clean_lines.append(';'.join(fields[:exception] + fields[start:]) + '\n')
                        else:
                            if end != 0:
                                clean_lines.append(';'.join(fields[:3] + fields[start:end]) + '\n')
                            else:
                                clean_lines.append(';'.join(fields[:3] + fields[start:]) + '\n')

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
    xls_file = [file for file in os.listdir(input_path) if file.endswith('.xls')]
    new_file = input_path  + '/temp.csv'

    for file in csv_files:
        f_input_path = f'{input_path}/{file}'
        f_output_path = f'{output_path}/{file}'

        # Encoding diferente
        if 'municipio_comunidad_madrid' in file:
            info_municipios(f_input_path=f_input_path, input_path=input_path, f_output_path=f_output_path)
        else:
            if selected_year == 2020:
                clean(f_input_path, f_output_path, selected_year=selected_year, start = -5, end = -4)
            clean(f_input_path, f_output_path, selected_year=selected_year, start = -2)

    for file in xls_file:
        pib_2020(file=file, input_path=input_path)
    
    return output_path


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
                    sector_data[sector][key] += float(row[3]) if row[3] else 0
                else:
                    # Si no existe, crear una nueva entrada en el diccionario
                    sector_data[sector][key] = float(row[3]) if row[3] else 0

        os.remove(file_path)

    # Escribir los datos sumados por sector en archivos CSV
    for sector, datos_sumados in sector_data.items():
        output_path = os.path.join(folder, f'{keyword}_{sector}.csv')

        with open(output_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            csv_writer.writerow(headers)
            for key, value in datos_sumados.items():
                csv_writer.writerow([key[0], key[1], key[2], value])


def refactor(example, input_file, output_file, row1: int, row2: int, name:int, headers_extra = []):
    
    data = {}

    with open(example, mode='r') as f_base:
        base_reader = csv.reader(f_base, delimiter=';')
        headers_base = next(base_reader)[:3]

        # Crear una clave única para cada entrada
        for row in base_reader:
            key = ';'.join(row[:3])
            data[key] = {}

    # Leer el segundo archivo y combinar los datos
    with open(input_file, mode='r') as f2:
        reader = csv.reader(f2, delimiter=';')
        next(reader)
        nombres = []
        for row in reader:
            nombre = row[name]
            nombres.append(nombre)
            for key in data:
                if nombre in key:
                    data[key] = row[row1:row2]

    # Escribir los datos sumados en un nuevo archivo CSV
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        
        # Escribir los encabezados
        headers = (headers_base[:3] + headers_extra)
        csv_writer.writerow(headers)

        # Escribir los datos sumados
        for key, values in data.items():
            line = [key.split(';')[0], key.split(';')[1], key.split(';')[2]] + [v if v != '' else '0' for v in values]
            # Añadir valores nulos para que todas las filas tengan el mismo número de datos
            while len(line) < len(headers):
                line.append('0')
            
            csv_writer.writerow(line)


def info_municipios(f_input_path, input_path, f_output_path):
    encoding, confidence = detect_encoding(f_input_path)
    new_file = input_path  + '/temp.csv'
    if not os.path.exists(new_file):
        with open(new_file, 'w'):
            pass
    # Usamos un documento de ejemplo
    example_path = './clean_data/otros_datos_poblacionales/densidad_poblacion.csv'
    if confidence > 0.5:
        convert_encoding(f_input_path, new_file, encoding)
        headers_extra = ['municipio_codigo_ine', 'zona_estadistica_codigo', 'zona_estadistica', 'superficie_km2']
        refactor(example_path, new_file, f_output_path, headers_extra=headers_extra, name=1, row1=3, row2=7)
        os.remove(new_file)

def pib_2020(input_path, file):
    f_input_path = f'{input_path}/{file}'
    new_file_path = xls_to_csv(f_input_path)
    output_folder = './clean_data_2020/pib_2020'
    output_path = f'{output_folder}/{os.path.basename(new_file_path)}'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Usamos un documento de ejemplo
    example_path = './clean_data/otros_datos_poblacionales/densidad_poblacion.csv'
    headers_extra = ['pib_primario', 'pib_secundario_1', 'pib_secundario_2', 'pib_terciario_1', 'pib_terciario_2', 'pib_terciario_3']
    clean(new_file_path, output_path=output_path , start=1, end= 6, exception=1)
    refactor(example=example_path, input_file=output_path, output_file=output_path, 
            headers_extra=headers_extra, row1=1, row2=7, name=0)
    os.remove(new_file_path)