# --------------- TRANSFORMED COMMA INDICATORS ------------------

# import pandas as pd

# # Paso 1: Leer los datos desde un archivo CSV
# df = pd.read_csv('dataset.csv', delimiter=';')

# df = df.drop(columns=['zona_estadistica', 'Serie', 'Codigo_municipio'])

# # Paso 2: Identificar las columnas clave
# df = df.rename(columns={'municipio_codigo_ine': 'lau_id'})
# key_columns = ['Nombre', 'lau_id']
# value_columns = [col for col in df.columns if col not in key_columns]

# rename_dict = {}
# indicador_value = 9

# for column in value_columns:
#     new_name = f"2.{indicador_value}"
#     rename_dict[column] = new_name
#     indicador_value += 1

# df = df.rename(columns=rename_dict)

# value_columns = [rename_dict[col] for col in value_columns]
# melted_df = pd.melt(df, id_vars=key_columns, value_vars=value_columns, 
#                     var_name='Indicador', value_name='Valor')

# melted_df['Year'] = 2023
# melted_df['Codigo_Valor'] = melted_df.apply(lambda row: f"{row['Indicador']}-2023-{row['lau_id']}", axis=1)

# orden = ['Codigo_Valor', 'Nombre', 'Valor', 'Year', 'Indicador', 'lau_id']

# final = pd.DataFrame()
# for o in orden:
#     final[o] = melted_df[o]

# final.to_csv('transformed_indicators.csv', index=False, sep=';')
# final.to_csv('transformed_comma_indicators.csv', index=False)

# print("Datos transformados y guardados en 'transformed_indicators.csv'.")

# --------------- DESCRIPTION INDICATORS ------------------

import pandas as pd

df = pd.read_json('descripcion_indicadores.json').T
df.reset_index(inplace=True)

indicador_value = 9
new_index_values = [f"2.{i}" for i in range(indicador_value, indicador_value + len(df))]
df['index'] = new_index_values

# Crear el DataFrame final
final = pd.DataFrame({
    'Bloque': [2] * len(df),
    'Variable': df['index'],
    'Nombre_bloque': ['DINAMISMO ECONÓMICO'] * len(df),
    'Nombre_variable': df['nombre_variable'],
    'Descripcion_variable': df['descripcion_variable'],
    'Fuente': df['Fuente'],
    'Unidad': df['Unidad']
})

final.to_csv('descripcion_comma_indicadores.csv', index=False)
final.to_csv('descripcion_indicadores.csv', sep=';', index=False)