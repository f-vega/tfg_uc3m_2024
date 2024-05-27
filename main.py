import os
from dataset_definition.clean_folder import clean_folder
from dataset_definition.sector_definition import sector_sum_folder
from dataset_definition.dataset import dataset
from dataset_definition.clustering import clustering
from dataset_definition.sector_prediction import sector_predictor
from dataset_definition.ratios import ratio_calculator

def main():
    input_folder = './original_data'
    clean_path = './clean_data'
    clean_path_2020 = './clean_data_2020'

    for folder_name in os.listdir(input_folder):
        # Combinar el nombre del directorio con la ruta base para obtener la ruta completa
        folder_path = os.path.join(input_folder, folder_name)

        if os.path.isdir(folder_path):
            if 'pib' in folder_path:
                output_path_2020 = clean_folder(folder_path, clean_path_2020, 2020)
            else:
                output_path = clean_folder(folder_path, clean_path)
                output_path_2020 = clean_folder(folder_path, clean_path_2020, 2020)
            if 'sector' in folder_path:
                keywords= output_path.split('/')[-1][:-7]
                sector_sum_folder(keyword=keywords, folder=output_path)
                sector_sum_folder(keyword=keywords, folder=output_path_2020)

    dataset_path = 'dataset.csv'
    dataset_2020 = 'dataset_2020.csv'
    dataset(clean_path, dataset_path)
    dataset(clean_path_2020, dataset_2020)
    clusters = ['zona_estadistica_codigo', 'densidad_poblacion', 'distancia_capital', 'poblacion_censada_total']
    for cluster in clusters:
        clustering(dataset_path, cluster)

    sector_predictor(dataset_2020=dataset_2020, dataset_2023=dataset_path)
    ratio_calculator(dataset_path, clusters)

if __name__=='__main__':
    main()