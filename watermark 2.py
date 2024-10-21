import glob
from PIL import Image, ImageFont, ImageDraw

font_path = "/System/Library/Fonts/Helvetica.ttf"
font_size = 20
color = (0,0,0)
offset_x = 100
offset_y = 50

font = ImageFont.truetype(font_path, font_size)
files = glob.glob("./*.jpg")

for i in range(len(files)):
    img = Image.open(files[i])
    width, height = img.size
    draw = ImageDraw.Draw(img)
    draw.text((width - offset_x, height - offset_y), files[i][2:-4], color, font=font)
    img.save("./watermark/" + files[i][2:])
