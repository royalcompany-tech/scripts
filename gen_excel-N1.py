import glob
from openpyxl import Workbook

URL_PREFIX = "https://www.royaljoyas.com.ar/wp-content/uploads/2020/10/"

workbook = Workbook()
sheet = workbook.active

files = glob.glob("./*.jpg")

for i in range(len(files)):
    sheet["A" + str(i + 1)] = files[i][2:-7]
    sheet["B" + str(i + 1)] = URL_PREFIX + files[i][2:]

workbook.save(filename="Nuevas.xlsx")
