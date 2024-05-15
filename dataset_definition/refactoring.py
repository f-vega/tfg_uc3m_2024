import os, csv
from dataset_definition.encoding import detect_encoding, convert_encoding, xls_to_csv
from dataset_definition.sector_definition import sector_definition_file
from dataset_definition.clean_file import clean
import pandas as pd

def refactor(input_file, output_file, row1: int, row2: int, name:int, headers_extra = []):
    
    data = {}

    example = './clean_data/otros_datos_poblacionales/densidad_poblacion.csv'

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
            line = [str(key.split(';')[0]), str(key.split(';')[1]), str(key.split(';')[2])] + [str(v) if v != '' else '0' for v in values]
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
    if confidence > 0.5:
        convert_encoding(f_input_path, new_file, encoding)
        headers_extra = ['municipio_codigo_ine', 'zona_estadistica_codigo', 'zona_estadistica', 'superficie_km2']
        refactor(new_file, f_output_path, headers_extra=headers_extra, name=1, row1=2, row2=6)
        os.remove(new_file)


def pib_2020(input_path, file, output_path):
    f_input_path = f'{input_path}/{file}'
    new_file_path = xls_to_csv(f_input_path)
    output_folder = f'{output_path}/pib_2020'
    output_path = f'{output_folder}/{os.path.basename(new_file_path)}'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Usamos un documento de ejemplo
    headers_extra = ['pib_primario', 'pib_secundario_1', 'pib_secundario_2', 'pib_terciario_1', 'pib_terciario_2', 'pib_terciario_3']
    clean(new_file_path, output_path=output_path , start=1, end= 6, exception=1)
    refactor(input_file=output_path, output_file=output_path, 
            headers_extra=headers_extra, row1=1, row2=7, name=0)
    sector_definition_file('pib', output_path)
    os.remove(new_file_path)

def parcelas_industriales(input_file):

    superficie_edificable = {}
    superficie_total = {}

    with open(input_file, mode='r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        
        for row in reader:
            municipio = row[0]
            codigo_municipio = row[1]
            uso_principal = row[2]
            try:
                superficie_edif = (float(row[3].replace(',', '.')))/100 # de ha a km2
            except ValueError:
                superficie_edif = 0.0
            
            try:
                superficie_total_actual = float(row[4].replace(',', '.'))/100 if row[4] else 0.0
            except ValueError:
                superficie_total_actual = 0.0
            
            # Actualizar la suma de superficies edificables y totales para el municipio y uso principal correspondientes
            if (municipio, codigo_municipio, uso_principal) in superficie_edificable:
                superficie_edificable[(municipio, codigo_municipio, uso_principal)] += superficie_edif
                superficie_total[(municipio, codigo_municipio, uso_principal)] += superficie_total_actual
            else:
                superficie_edificable[(municipio, codigo_municipio, uso_principal)] = superficie_edif
                superficie_total[(municipio, codigo_municipio, uso_principal)] = superficie_total_actual

    # Crear un diccionario para almacenar los datos combinados
    join_data = {}

    # Iterar sobre los datos de uso industrial
    for (municipio, codigo_municipio, uso_principal), superficie_edif in superficie_edificable.items():
        if uso_principal == 'T' or uso_principal == 'I':
            key = (municipio, codigo_municipio)
            if key not in join_data:
                join_data[key] = {'Municipio': municipio, 'codigo_municipio': codigo_municipio}
            if uso_principal == 'I':
                join_data[key]['superficie_edificable_industrial'] = round(superficie_edif, 2)
                join_data[key]['superficie_total_industrial'] = round(superficie_total[(municipio, codigo_municipio, uso_principal)], 2)
            elif uso_principal == 'T':
                join_data[key]['superficie_edificable_terciario_industrial'] = round(superficie_edif, 2)
                join_data[key]['superficie_total_terciario_industrial'] = round(superficie_total[(municipio, codigo_municipio, uso_principal)], 2)

    # Crear un diccionario para almacenar los datos combinados
    join_data = {}

    # Iterar sobre los datos de uso industrial
    for (municipio, codigo_municipio, uso_principal), superficie_edif in superficie_edificable.items():
        if uso_principal == 'T' or uso_principal == 'I': # Solo uso industrial y terciario industrial
            key = (municipio, codigo_municipio)
            if key not in join_data:
                join_data[key] = {'Municipio': municipio, 'codigo_municipio': codigo_municipio}
            if uso_principal == 'I':
                join_data[key]['sup_edif_indust'] = round(superficie_edif, 2)
                join_data[key]['sup_total_indust'] = round(superficie_total[(municipio, codigo_municipio, uso_principal)], 2)
            elif uso_principal == 'T':
                join_data[key]['sup_edif_terc_indust'] = round(superficie_edif, 2)
                join_data[key]['sup_total_terc_indust'] = round(superficie_total[(municipio, codigo_municipio, uso_principal)], 2)

    # Escribir los datos combinados en un nuevo archivo CSV
    with open(input_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        for municipio_data in join_data.values():
            writer.writerow(municipio_data.values())

    headers_extra = ['sup_edif_indust', 'sup_total_indust', 'sup_edif_terc_indust', 'sup_total_terc_indust']
    refactor(headers_extra=headers_extra, input_file=input_file, output_file=input_file, row1=2, row2=6, name=0)
