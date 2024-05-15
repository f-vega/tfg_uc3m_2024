import scipy.stats
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Crear algunos datos de ejemplo
data = np.random.randn(100, 5)
labels = np.random.randint(0, 2, 100)

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

print("Todas las bibliotecas están funcionando correctamente.")
