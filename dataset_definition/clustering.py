import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def clustering(input_file, cluster_variable):
    data = pd.read_csv(input_file, delimiter=';', dtype={'codigo_municipio_ine': str})
    clustering_data = data[data['Nombre'] != 'Madrid'][data['Serie'] == 'Municipios'][['Nombre', 'zona_estadistica', 'zona_estadistica_codigo', 
                                                                                       'densidad_poblacion', 'distancia_capital']]

    features = clustering_data[[cluster_variable]]
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Confirmar la normalización
    features_scaled.mean(axis=0), features_scaled.std(axis=0)

    X = features_scaled
    X_train, X_test = train_test_split(X, test_size=0.3, random_state=42)
    # kmeans_clusters(features_scaled)

    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X_train)

    # test_labels = kmeans.predict(X_test)
    labels = kmeans.predict(X)
    cluster_name = 'cluster_' + str(cluster_variable.split('_')[0]) + '_' + str(cluster_variable.split('_')[1])

    rows_exist = data.index.isin(clustering_data.index)
    data.loc[rows_exist, cluster_name] = labels


    silhouette = silhouette_score(X, labels, metric='euclidean')
    print(f'Coherencia: {silhouette}')
    data.to_csv('dataset.csv', index=False, sep=';')
    # # Mostrar el gráfico



def plt_scatterplot(x, y, hue, data, title='', xlabel='', ylabel='', figsize=(10, 6), palette='viridis', s=100):
    plt.figure(figsize=figsize)
    sns.scatterplot(x=x, y=y, hue=hue, data=data, palette=palette, s=s, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


def kmeans_clusters(features):
    sse = []
    k_values = range(1, 11)
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(features)
        sse.append(kmeans.inertia_)
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, sse, marker='o')
    plt.title('El Método del Codo para Determinar k')
    plt.xlabel('Número de Clusters (k)')
    plt.ylabel('Suma de Cuadrados Dentro de los Clusters')
    plt.grid(True)
    # plt.show()
