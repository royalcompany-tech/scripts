import shutil, textract, re, os, glob
from PIL import Image, ImageFont, ImageDraw

font_path = "/System/Library/Fonts/Helvetica.ttf"
font_size = 20
color = (0,0,0)
offset_x = 100
offset_y = 25

font = ImageFont.truetype(font_path, font_size)

inputfile = "/Users/franciscodanielgomez/Desktop/Nota.pdf"
pedido = ""
imagenes = "/Users/franciscodanielgomez/Desktop/Puto/"
text = textract.process(inputfile)

# Nombre del archivo
prog = re.compile("fono\\\\n\\\\n (\w+)\\\\n")
pedido = prog.findall(str(text))[0]
os.mkdir(pedido)

# Codigo del producto
prog = re.compile("SKU: (\w+)")
products = prog.findall(str(text))

for product in products:
    shutil.copy2(imagenes + product + ".jpg", pedido)

files = glob.glob(imagenes + "*.jpg")

for i in range(len(files)):
    img = Image.open(files[i])
    width, height = img.size
    draw = ImageDraw.Draw(img)
    draw.text((width - offset_x, height - offset_y), files[i][2:-4], color, font=font)
    img.save(files[i])
