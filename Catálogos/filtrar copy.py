import pandas as pd

# Cargar los dos archivos CSV
tabla_completa = pd.read_csv('tabla_completa.csv')
lista_sku = pd.read_csv('lista_sku.csv')

# Filtrar la tabla completa para que solo incluya los SKU en la lista
tabla_filtrada = tabla_completa[tabla_completa['SKU'].isin(lista_sku['SKU'])]

# Guardar el resultado en un nuevo archivo CSV
tabla_filtrada.to_csv('tabla_filtrada.csv', index=False)

print("Se ha creado 'tabla_filtrada.csv' con los SKU filtrados.")
