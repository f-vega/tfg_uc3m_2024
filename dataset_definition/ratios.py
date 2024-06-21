import pandas as pd
import numpy as np

def ratio_calculator(input_path, clusters):
    
    data = pd.read_csv(input_path, delimiter=';', encoding='utf-8', dtype={'Codigo_municipio': str})
    data = data[(data['Nombre'] != 'Madrid') & (data['Serie'] == 'Municipios')]
    grupos_edad_activos = ['poblacion_censada_{}a{}'.format(i, i+4) for i in range(15, 65, 5)]
    data['poblacion_activa'] = data[grupos_edad_activos].sum(axis=1)

    total_columns = ['contratos', 'unidades_productivas', 'empleo']
    for column in total_columns:
        col_name = f'{column}_total'
        data[col_name] = data[f'{column}_primario'] + data[f'{column}_secundario'] + data[f'{column}_terciario']

    # Crear DataFrame de ratios
    data_ratios = pd.DataFrame()
    data_ratios['Nombre'] = data['Nombre']
    data_ratios['ratio_contratos_por_poblacion_activa'] = np.where(
        data['poblacion_activa'] != 0,
        round(data['contratos_total'] / data['poblacion_activa'], 3),
        0
    )
    print(data_ratios)

    data_ratios['ratio_empleo_por_poblacion_activa'] = np.where(
        data['poblacion_activa'] != 0,
        round(data['empleo_total'] / data['poblacion_activa'], 3),
        0
    )
    data_ratios['ratio_contratos_por_up'] = np.where(
        data['unidades_productivas_total'] != 0,
        round(data['contratos_total'] / data['unidades_productivas_total'], 3),
        0
    )
    data_ratios['ratio_paro_por_poblacion_activa'] = np.where(
        data['poblacion_activa'] != 0,
        round(data['paro_registrado_total'] / data['poblacion_activa'], 3),
        0
    )
    data_ratios['ratio_empleo_por_paro'] = np.where(
        data['contratos_total'] != 0,
        round(data['empleo_total'] / data['paro_registrado_total'], 3),
        0
    )
    
    # Ratios por sector de actividad
    sectores = ['primario', 'secundario', 'terciario']
    for sector in sectores:
        data_ratios[f'ratio_contratos_{sector}_por_poblacion_activa'] = np.where(
            data['poblacion_activa'] != 0,
            round(data[f'contratos_{sector}'] / data['poblacion_activa'], 3),
            0
        )
        data_ratios[f'ratio_empleo_{sector}_por_poblacion_activa'] = np.where(
            data['poblacion_activa'] != 0,
            round(data[f'empleo_{sector}'] / data['poblacion_activa'], 3),
            0
        )
    
    # Ratios por grupo de edad
    for edad in grupos_edad_activos:
        data_ratios[f'ratio_contratos_por_{edad}'] = np.where(
            data[edad] != 0,
            round(data['contratos_total'] / data[edad], 3),
            0
        )
        data_ratios[f'ratio_empleo_por_{edad}'] = np.where(
            data[edad] != 0,
            round(data['empleo_total'] / data[edad], 3),
            0
        )
        data_ratios[f'ratio_paro_por_{edad}'] = np.where(
            data[edad] != 0,
            round(data['paro_registrado_total'] / data[edad], 3),
            0
        )
    
    # Ratio de unidades productivas por población activa
    data_ratios['ratio_up_por_poblacion_activa'] = np.where(
        data['poblacion_activa'] != 0,
        round(data['unidades_productivas_total'] / data['poblacion_activa'], 3),
        0
    )

    data_ratios.drop(columns=['Nombre'], inplace=True)
    dataset = data_ratios.copy()
    for cluster in clusters:
        cluster_col = f'cluster_{cluster.split("_")[0]}_{cluster.split("_")[1]}'
        data_ratios[cluster_col] = data[cluster_col]
        dataset[cluster_col] = data[cluster_col]
        cluster_ratios_means = round(data_ratios.groupby(cluster_col).mean(), 3)
        cluster_ratios_means = cluster_ratios_means.add_suffix(f'_mean_{cluster_col}')
        dataset = dataset.merge(cluster_ratios_means, left_on=cluster_col, right_index=True, how='left')
        data_ratios.drop(columns=[cluster_col], inplace=True)
        
    # Añadir las columnas Serie, Codigo_municipio y Nombre
    dataset['Serie'] = data['Serie']
    dataset['Codigo_municipio'] = data['Codigo_municipio']
    dataset['Nombre'] = data['Nombre']

    first_columns = ['Serie', 'Codigo_municipio', 'Nombre']
    all_columns = first_columns + [col for col in dataset.columns if col not in first_columns]
    dataset = dataset[all_columns]

    # Combinamos los DataFrames data y dataset solo añadiendo las nuevas columnas de dataset
    combined_columns = [col for col in dataset.columns if col not in data.columns]
    data_combined = pd.concat([data, dataset[combined_columns]], axis=1)
    print(len(data_combined.columns))
    data_combined.to_csv(input_path, sep=';', index=False, encoding='utf-8')
    print(f"Dataset con ratios guardado en {input_path}")