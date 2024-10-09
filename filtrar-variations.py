import pandas as pd

# Cargar los CSV en DataFrames
df_10 = pd.read_csv('10.csv')  # Este contiene la lista completa de productos
df_20 = pd.read_csv('20.csv')  # Este contiene la lista de SKU

# Convertir la columna SKU de 20.csv en una lista
sku_list = df_20['SKU'].tolist()

# Filtrar las filas de 10.csv donde el valor de la columna 'Superior' coincida con algún SKU de la lista
df_filtered = df_10[df_10['Superior'].isin(sku_list)]

# Guardar el resultado en un nuevo archivo CSV
df_filtered.to_csv('filtrado_superior.csv', index=False)

print("Archivo 'filtrado_superior.csv' generado con éxito.")
