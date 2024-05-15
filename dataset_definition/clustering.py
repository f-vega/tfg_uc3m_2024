import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


import sklearn
print (sklearn.__version__)

def clustering(input_file, cluster_variable):
    data = pd.read_csv(input_file, delimiter=';')
    clustering_data = data[data['Nombre'] != 'Madrid'][data['Serie'] == 'Municipios'][['Nombre', 'zona_estadistica', 'zona_estadistica_codigo', 'densidad_poblacion', 'distancia_capital']]
    print(clustering_data)

    # plt_figures

    features = clustering_data[cluster_variable]
    # Normalización de los datos
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Confirmar la normalización
    features_scaled.mean(axis=0), features_scaled.std(axis=0)

    X = features_scaled
    X_train, X_test = train_test_split(X, test_size=0.3, random_state=42)

    

def plt_figures(data, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x, y=y, data=data, alpha=0.6, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)
    plt.grid(True)
    # plt.show()