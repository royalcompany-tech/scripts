import pandas as pd
from fpdf import FPDF
from io import BytesIO
import requests
import os
from PIL import Image
from collections import defaultdict
from datetime import datetime

def download_and_convert_image(image_url, output_filename):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        img.save(output_filename, 'JPEG')
        return output_filename
    except Exception as e:
        print(f"Error al descargar o convertir la imagen {image_url}: {e}")
        return None

# Leer y filtrar el CSV
csv_file = 'wc-product-export-5-9-2024-1725558304869.csv'
df = pd.read_csv(csv_file)
df['Inventario'] = pd.to_numeric(df['Inventario'], errors='coerce')
df_filtered = df[(df['Publicado'] == 1) & 
                 ((df['Inventario'] > 1) | df['Inventario'].isna()) & 
                 (df['Tipo'].isin(['simple', 'variable']))].copy()
df_filtered['Primera_Imagen'] = df_filtered['Imágenes'].apply(
    lambda x: x.split(',')[0].strip() if isinstance(x, str) else ''
)

# Configuración de la página
page_width = 210
page_height = 297
margin = 10

# Configuración de la celda
columns = 2
rows = 3
cell_width = (page_width - 2 * margin) / columns
cell_height = (page_height - 2 * margin) / rows

# Configuración de la imagen
image_height = cell_height * 0.5  # Reducido para dejar espacio para los precios
image_width = image_height

class CatalogPDF(FPDF):
    def header(self):
        self.set_font('Arial', '', 8)
        self.cell(0, 10, 'Catálogo', 0, 1, 'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def add_category_page(self, category):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(0, 0, category, 0, 1, 'C')

    def add_product(self, x, y, product):
        self.set_xy(x, y)
        
        # Imagen
        img_filename = f"temp_image_{product.name}.jpg"
        converted_img = download_and_convert_image(product['Primera_Imagen'], img_filename)
        if converted_img:
            with Image.open(converted_img) as img:
                orig_width, orig_height = img.size
                aspect_ratio = orig_width / orig_height
                new_width = min(image_height * aspect_ratio, cell_width * 0.9)
                new_height = new_width / aspect_ratio
                
                img_x = x + (cell_width - new_width) / 2
                img_y = y + (image_height - new_height) / 2
                
                self.image(converted_img, img_x, img_y, new_width, new_height)
            os.remove(converted_img)
        else:
            self.set_xy(x + (cell_width - image_width) / 2, y)
            self.cell(image_width, image_height, 'Imagen no disponible', 1, 1, 'C')
        
        # Nombre del producto y precios
        self.set_xy(x, y + image_height + 2)
        self.set_font('Arial', 'B', 8)
        nombre = str(product['Nombre'])
        precio_normal = product['Precio normal']
        precio_rebajado = product['Precio rebajado']
        
        if pd.notna(precio_normal) or pd.notna(precio_rebajado):
            if pd.notna(precio_normal) and pd.notna(precio_rebajado):
                precio_texto = f" - ${precio_normal} ${precio_rebajado}"
            elif pd.notna(precio_normal):
                precio_texto = f" - ${precio_normal}"
            else:
                precio_texto = f" - ${precio_rebajado}"
            nombre_con_precio = f"{nombre}{precio_texto}"
        else:
            nombre_con_precio = nombre
        
        self.multi_cell(cell_width, 4, nombre_con_precio, 0, 'C')
        
        # SKU
        self.set_xy(x, self.get_y())
        self.set_font('Arial', '', 7)
        self.cell(cell_width, 4, f"SKU: {product['SKU']}", 0, 1, 'C')
        
        # Atributos
        self.set_xy(x, self.get_y())
        self.set_font('Arial', 'I', 7)
        attributes = []
        if pd.notna(product['Nombre del atributo 1']) and pd.notna(product['Valor(es) del atributo 1']):
            attributes.append(f"{product['Nombre del atributo 1']}: {product['Valor(es) del atributo 1']}.")
        if pd.notna(product['Nombre del atributo 2']) and pd.notna(product['Valor(es) del atributo 2']):
            attributes.append(f"{product['Nombre del atributo 2']}: {product['Valor(es) del atributo 2']}.")
        attributes_text = ' '.join(attributes)
        self.multi_cell(cell_width, 3, attributes_text, 0, 'C')

def extract_categories(categories_str):
    categories = categories_str.split(', ')
    for category in categories:
        parts = category.split(' > ')
        if len(parts) == 3:
            return parts[1], parts[2]  # Retorna (categoría, subcategoría)
    return None, None

# Organizar productos por categoría y subcategoría
product_categories = defaultdict(lambda: defaultdict(list))
for _, product in df_filtered.iterrows():
    category, subcategory = extract_categories(product['Categorías'])
    if category and subcategory:
        product_categories[category][subcategory].append(product)

# Crear PDF
pdf = CatalogPDF()
pdf.set_auto_page_break(auto=True, margin=margin)

for category, subcategories in product_categories.items():
    pdf.add_category_page(category)
    
    for subcategory, products in subcategories.items():
        pdf.add_category_page(subcategory)
        
        for i, product in enumerate(products):
            if i % (columns * rows) == 0 and i > 0:
                pdf.add_page()
            
            col = i % columns
            row = (i // columns) % rows
            
            x = margin + col * cell_width
            y = margin + row * cell_height + 15
            
            pdf.add_product(x, y, product)
            
            # Mostrar progreso
            print(f"Añadiendo producto {i+1} de {len(products)} en {category} > {subcategory}")

# Obtener la fecha actual en formato YYYYMMDD
fecha_actual = datetime.now().strftime('%Y%m%d')

# Crear el nombre del archivo usando la fecha
output_filename = f"catalogo-con-precio-{fecha_actual}.pdf"

# Guardar el PDF
pdf.output(output_filename)

print(f"PDF generado exitosamente como {output_filename}.")
