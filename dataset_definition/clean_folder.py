import os, shutil
from dataset_definition.clean_file import clean
from dataset_definition.refactoring import info_municipios, pib_2020, parcelas_industriales, poblacion_2020

def clean_folder(input_path, output_folder, selected_year=2023):
    output_path = f'{output_folder}/{os.path.basename(input_path)}'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    csv_files = [file for file in os.listdir(input_path) if file.endswith('.csv')]
    xls_file = [file for file in os.listdir(input_path) if file.endswith('.xls')]

    for file in csv_files:
        f_input_path = f'{input_path}/{file}'
        f_output_path = f'{output_path}/{file}'

        # Encoding diferente
        if 'municipio_comunidad_madrid' in file:
            # info_municipios(f_input_path=f_input_path, input_path=input_path, f_output_path=f_output_path)
            pass

        elif 'parcela' in file:
             clean(f_input_path, f_output_path)
             parcelas_industriales(f_output_path)

        elif 'poblacion_censada' in file:
            if '2020' in file and selected_year == 2023:
                pass
            elif '2020' in file and selected_year == 2020:
                poblacion_2020(f_input_path, f_output_path)
            elif selected_year == 2020:
                pass
            else:
                clean(f_input_path, f_output_path, selected_year=2023, start = -2)
        
        elif selected_year == 2020 and 'distancia_capital' not in file and 'explotaciones' not in file:
            clean(f_input_path, f_output_path, selected_year=selected_year, start = -5, end = -4)
        else:
            clean(f_input_path, f_output_path, selected_year=selected_year, start = -2)

    for file in xls_file:
        pib_2020(file=file, input_path=input_path, output_path=output_folder)

    return output_path