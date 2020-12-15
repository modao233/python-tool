from PIL import Image
import os

input = './input/'
output = './output/'

a = os.listdir(input)

for i in a:
    I = Image.open(input+i)
    L = I.convert('1')
    #L = I.convert('L')
    L.save(output+i)