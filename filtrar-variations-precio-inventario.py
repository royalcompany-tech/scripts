import pandas as pd
import numpy as np

# Cargar los CSV en DataFrames
df_10 = pd.read_csv('10.csv')  # Este contiene la lista completa de productos
df_20 = pd.read_csv('40.csv')  # Este contiene la lista de SKU y precios

# Filtrar las filas de 10.csv donde el valor de la columna 'Superior' coincida con algún SKU de 20.csv
df_filtered = df_10[df_10['Superior'].isin(df_20['SKU'])]

# Combinar los dos DataFrames en base a la columna 'Superior' en df_10 y 'SKU' en df_20
df_combined = df_filtered.merge(df_20, how='left', left_on='Superior', right_on='SKU')

# Comprobar qué columnas existen después del merge
print("Columnas disponibles después del merge:", df_combined.columns)

# Agrupar por el valor de 'Superior' (SKU principal) y realizar el cálculo del inventario
def distribuir_inventario(grupo):
    inventario_total = grupo['Inventario_x'].sum()  # Sumar el inventario del grupo desde la columna correcta
    cantidad_variaciones = len(grupo)  # Contar las filas (variaciones) en el grupo
    inventario_por_variacion = np.floor(inventario_total / cantidad_variaciones)  # Dividir y redondear hacia abajo
    grupo['Inventario_x'] = inventario_por_variacion  # Asignar el inventario distribuido a cada fila
    return grupo

# Aplicar la distribución de inventario por cada grupo de 'Superior'
df_combined = df_combined.groupby('Superior').apply(distribuir_inventario)

# Guardar el resultado en un nuevo archivo CSV
df_combined.to_csv('filtrado_con_precios_e_inventario.csv', index=False)

print("Archivo 'filtrado_con_precios_e_inventario.csv' generado con inventario distribuido por variación.")
