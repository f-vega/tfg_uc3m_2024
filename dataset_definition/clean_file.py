
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
                if 'Sin Zona asignada   'in line:
                    delete = True
                if '(A)' in line:
                    line = line.replace('(A) Avance ;', '')
                    fields = line.strip().split(';')
                elif '-' in line and not delete_next:
                    for i, field in enumerate(fields):
                        if i >= 3 and field == '-':
                            fields[i] = '0'
                if 'parcelas' in input_path:
                    if len(fields) <= 12 or not fields[3].isdigit():
                        delete = True
                if not delete:
                        if 'parcelas' in input_path:
                            clean_lines.append(';'.join([str(x) for x in [fields[4], fields[3], fields[9]] + fields[11:13]]) + '\n')
                        else:
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