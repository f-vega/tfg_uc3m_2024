# --------------- TRANSFORMED COMMA INDICATORS ------------------

import pandas as pd
import re

def name_transform(nombre):
    if nombre == 'Álamo, El':
        new_name = 'Alamo (El)'
        return new_name
    patron = re.compile(r'^(.+),\s*(La|Las|El|Los)$')
    if patron.match(nombre):
        reemplazo = r'\1 (\2)'
        return patron.sub(reemplazo, nombre)
    else:
        return nombre
    

# Paso 1: Leer los datos desde un archivo CSV
data = pd.read_csv('../dataset.csv', delimiter=';', index_col=False)

laus = pd.read_csv('../MadridLAUGeometries.csv', index_col=False, dtype={'lau_id': str}, encoding='utf-8')

laus = laus.rename(columns={'lau_name': 'Nombre'})

laus['Nombre'] = laus['Nombre'].apply(name_transform)
laus = laus.replace('Álamo', 'Alamo')

data = data.drop(columns=['zona_estadistica', 'Serie', 'Codigo_municipio', 'municipio_codigo_ine'])

df = pd.merge(data, laus[['Nombre', 'lau_id']], on='Nombre', how='left')

# Paso 2: Identificar las columnas clave
key_columns = ['Nombre', 'lau_id']
value_columns = [col for col in df.columns if col not in key_columns]

with open('indicators.txt', 'w') as file:
    for col in value_columns:
        file.write(col + '\n')

rename_dict = {}
indicador_value = 9

for column in value_columns:
    new_name = f"2.{indicador_value}"
    rename_dict[column] = new_name
    indicador_value += 1

df = df.rename(columns=rename_dict)

value_columns = [rename_dict[col] for col in value_columns]
melted_df = pd.melt(df, id_vars=key_columns, value_vars=value_columns, 
                    var_name='Indicador', value_name='Valor')

melted_df['Year'] = 2023
melted_df['Codigo_Valor'] = melted_df.apply(lambda row: f"{row['Indicador']}-2023-{row['lau_id']}", axis=1)

orden = ['Codigo_Valor', 'Nombre', 'Valor', 'Year', 'Indicador', 'lau_id']

final = pd.DataFrame()
for o in orden:
    final[o] = melted_df[o]

final.to_csv('transformed_indicators.csv', index=False, sep=';')
final.to_csv('transformed_comma_indicators.csv', index=False)

print("Datos transformados y guardados en 'transformed_indicators.csv'.")

# --------------- DESCRIPTION INDICATORS ------------------

# import pandas as pd

# df = pd.read_json('descripcion_indicadores.json').T
# df.reset_index(inplace=True)

# indicador_value = 9
# new_index_values = [f"2.{i}" for i in range(indicador_value, indicador_value + len(df))]
# df['index'] = new_index_values

# # Crear el DataFrame final
# final = pd.DataFrame({
#     'Bloque': [2] * len(df),
#     'Variable': df['index'],
#     'Nombre_bloque': ['DINAMISMO ECONÓMICO'] * len(df),
#     'Nombre_variable': df['nombre_variable'],
#     'Descripcion_variable': df['descripcion_variable'],
#     'Fuente': df['Fuente'],
#     'Unidad': df['Unidad']
# })

# final.to_csv('descripcion_comma_indicadores.csv', index=False)
# final.to_csv('descripcion_indicadores.csv', sep=';', index=False)