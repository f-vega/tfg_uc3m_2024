import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer


def sector_predictor(dataset_2023, dataset_2020, ):
# Leer los datos
    data_2023 = pd.read_csv(dataset_2023, delimiter=';', dtype={'Codigo_municipio': str})
    data_2020 = pd.read_csv(dataset_2020, delimiter=';', dtype={'superficie_km2': float})

    # Selecciona las columnas deseadas
    selected_columns = data_2020.columns

    # Selecciona las columnas deseadas del DataFrame de municipios
    train_data = data_2020[data_2020['Serie'] == 'Municipios'][data_2020['Nombre'] != 'Madrid'].iloc[:, 6:]
    test_data = data_2023[data_2023['Serie'] == 'Municipios'][data_2023['Nombre'] != 'Madrid'].iloc[:, 6:]
    test_data = test_data[selected_columns.intersection(test_data.columns)]
    join_data = data_2023[data_2023['Serie'] == 'Municipios'][data_2023['Nombre'] != 'Madrid'].iloc[:, :6]

    X_train = train_data.drop(columns=['sector_principal'])
    y_train = train_data['sector_principal']

    # Codificar la variable categórica 'sector'
    label_encoder = LabelEncoder()
    train_data['sector_encoded'] = label_encoder.fit_transform(train_data['sector_principal'])

    # Dividir datos en variables independientes y dependiente
    X = train_data.drop(['sector_principal', 'sector_encoded'], axis=1)
    y = train_data['sector_encoded']

    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear un imputador para reemplazar los valores faltantes con la media
    imputer = SimpleImputer(strategy='mean')

    # Aplicar el imputador a tus datos de entrenamiento
    X_train_imputed = imputer.fit_transform(X_train)


    # Entrenamiento del modelo (Random Forest Classifier como ejemplo)
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train_imputed, y_train)


    # Aplicar el mismo imputador a tus datos de prueba
    X_test_imputed = imputer.transform(X_test)

    # Realizar predicciones en tus datos de prueba imputados
    # Validación del modelo
    y_pred = rf_model.predict(X_test_imputed)
    print(classification_report(y_test, y_pred))


    # Preprocesamiento similar al de los datos del 2020
    data_predict_imputed = imputer.transform(test_data)

    nan_indices = np.isnan(data_predict_imputed).any(axis=0)
    columnas_con_nan = np.where(nan_indices)[0]


    # Predecir el sector para el año 2023
    predictions_2023 = rf_model.predict(data_predict_imputed)

    # Decodificar las predicciones si es necesario
    predictions_decoded = label_encoder.inverse_transform(predictions_2023)

    # Agregar las predicciones al dataframe de 2023
    test_data['sector_principal'] = predictions_decoded

    test_data.to_csv('prueba.csv', sep=';', index=False)