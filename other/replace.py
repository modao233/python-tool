import os

with open('图书馆书睿之家.txt', 'r', encoding='utf-8') as f:
    text = f.read()

with open('图书馆整理.txt', 'w', encoding='utf-8') as w:
    w.write(text.replace('|', '\n'))

f.close()
w.close()

