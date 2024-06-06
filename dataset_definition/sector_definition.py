import os, csv
import pandas as pd

def sector_sum_folder(keyword, folder):
    sector_data = {'primario': {}, 'secundario': {}, 'terciario': {}}

    for sector in sector_data.keys():
        output_path = os.path.join(folder, f'{keyword}_{sector}.csv')
        if os.path.exists(output_path):
            with open(output_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow([])

    if not os.path.exists(folder):
        os.makedirs(folder)
    csv_files = os.listdir(folder)
    csv_files = [file for file in csv_files if file.endswith('.csv')]

    for file in csv_files:
        sector = sector_def(file)
        file_path = os.path.join(folder, file)

        with open(os.path.join(folder, file), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            headers = next(csv_reader)
            for row in csv_reader:
                serie = row[0] if row else ''
                codigo_municipio = row[1] if len(row) > 1 else ''
                nombre = row[2] if len(row) > 2 else ''

                key = (serie, codigo_municipio, nombre)
                if key in sector_data[sector]:
                    sector_data[sector][key] += float(row[3]) if row[3] != '' else 0

                else:
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

def sector_definition_file(keyword, input_file):
    file = pd.read_csv(input_file, delimiter=';', dtype={'Codigo_municipio': str})
    sectors = ['primario', 'secundario', 'terciario']
    for column in file.columns:
        for sector in sectors:
            if sector in column:
                column_name = f'{keyword}_{sector}'
                if sector != 'primario':
                    if column_name in file.columns:
                        file[column_name] += file[column]
                        file[column_name] = round(file[column_name], 3)
                    else:
                        file[column_name] = file[column]
                    del(file[column])
    for index, row in file.iterrows():
        max_sector_value = max(row[f'pib_{sector}'] for sector in sectors)
        for sector in sectors:
            if row[f'pib_{sector}'] == max_sector_value:
                file.loc[index, 'sector_principal'] = sector

    file.to_csv(input_file, index=False, sep=';')

def sector_def(file):
    primario_keywords = ['agricultura', 'ganaderia', 'pesca', 'primario']
    secundario_keywords = ['industria', 'construccion', 'electricidad', 'agua', 'metalurgia', 'secundario']

    if any(keyword in file for keyword in primario_keywords):
        sector = 'primario'
    elif any(keyword in file for keyword in secundario_keywords):
        sector = 'secundario'
    else:
        sector = 'terciario'

    if sector:
        return sector
    else:
        return None
