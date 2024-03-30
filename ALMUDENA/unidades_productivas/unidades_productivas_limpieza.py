import os
# -------------------- LIMPIEZA DE LOS CSVS --------------------

def clean_and_save_to_new_folder(input_folder, output_folder, texto_inicial='Avance'):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Obtener la lista de archivos CSV en la carpeta de entrada
    archivos_csv = [archivo for archivo in os.listdir(input_folder) if archivo.endswith('.csv')]

    # Limpiar y guardar los archivos CSV en la carpeta de salida
    for archivo in archivos_csv:
        archivo_original = os.path.join(input_folder, archivo)
        archivo_limpiado = os.path.join(output_folder, archivo)
        with open(archivo_original, 'r') as f_input, open(archivo_limpiado, 'w') as f_output:
            eliminar = False
            for line in f_input:
                if texto_inicial in line:
                    eliminar = True
                if not eliminar:
                    f_output.write(line)
                if line.strip() == "":
                    eliminar = False

# Rutas de las carpetas de entrada y salida
input_folder = ".\original_data"
output_folder = ".\clean_data"

# Limpiar y guardar los archivos CSV en la nueva carpeta
clean_and_save_to_new_folder(input_folder, output_folder)
