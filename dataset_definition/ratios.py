import pandas as pd

def ratio_calculator(input_path, clusters):
    data = pd.read_csv( input_path, delimiter=';', encoding='latin-1', dtype={'Codigo_municipio': str})
    data = data[(data['Nombre'] != 'Madrid') & (data['Nombre'] != 'Municipio de Madrid')]
    data_ratios = pd.DataFrame()

    # Zonas estadísticas primero por comodidad
    data = data.sort_values(by='Serie', ascending=False)

    grupos_edad_activos = ['poblacion_censada_{}a{}'.format(i, i+4) for i in range(15, 65, 5)]
    data['poblacion_activa'] = data[grupos_edad_activos].sum(axis=1)

    total_columns = ['contratos', 'unidades_productivas']
    for column in total_columns:
        col_name = f'{column}_total'
        data[col_name] = data[f'{column}_primario'] + data[f'{column}_secundario'] + data[f'{column}_terciario']

    # Ratio de contratos por población censada
    data_ratios['ratio_contratos_por_poblacion'] = round(data['contratos_total'] / data['poblacion_activa'], 3)

    # Ratio de contratos por unidad productiva
    data_ratios['ratio_contratos_por_up'] = round(data['contratos_total'] / data['unidades_productivas_total'], 3)

    # Ratio de paro registrado por población
    data_ratios['ratio_paro_por_poblacion_activa'] = round(data['paro_registrado_total'] / data['poblacion_activa'], 3)

    # Ratio de paro registrado por contrato
    data_ratios['ratio_paro_por_contrato'] = round(data['paro_registrado_total'] / data['contratos_total'], 3)

    # Ratio de contratos por sector de actividad
    data_ratios['ratio_contratos_primario'] = round(data['contratos_primario'] / data['poblacion_activa'], 3)
    data_ratios['ratio_contratos_secundario'] = round(data['contratos_secundario'] / data['poblacion_activa'], 3)
    data_ratios['ratio_contratos_terciario'] = round(data['contratos_terciario'] / data['poblacion_activa'], 3)

    # Ratio de contratos y paro por grupo de edad
    for edad in grupos_edad_activos:
        data_ratios[f'ratio_contratos_por_{edad}'] = round(data['contratos_total'] / data[edad], 3)
        data_ratios[f'ratio_paro_por_{edad}'] = round(data['paro_registrado_total'] / data[edad], 3)

    # Ratio de unidades productivas por pirámide poblacional
    data_ratios['ratio_up_por_poblacion_activa'] = round(data['unidades_productivas_total'] / data['poblacion_activa'], 3)

    'cluster_zona_estadistica;cluster_densidad_poblacion;cluster_distancia_capital'
    # data.to_csv(input_path, sep=';', index=False)
    data_ratios['cluster_zona_estadistica'] = data['cluster_zona_estadistica']
    data_ratios['cluster_densidad_poblacion'] = data['cluster_densidad_poblacion'] 
    data_ratios['cluster_distancia_capital'] = data['cluster_distancia_capital'] 
    data_ratios['cluster_poblacion_censada'] = data['cluster_poblacion_censada'] 

    for cluster in clusters:
        cluster = f'cluster_{cluster.split("_")[0]}_{cluster.split("_")[1]}'
        cluster_ratios_means = data_ratios.groupby(cluster).mean()
        print(cluster_ratios_means)
    
    cluster_ratios_means.to_csv('..\prueba.csv', sep=';')



    
    


