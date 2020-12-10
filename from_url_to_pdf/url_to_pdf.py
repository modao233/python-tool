## 可配合 gongzhonghao.py 使用
## 载完微信公众号的文章链接，现在需要将其打印输出成pdf文件

import pdfkit
import re
import time

titles = ''
urls = ''

## 读全部行，统计行数，读完句柄会失效，需要重新open
lines = len(open('xxx.txt', 'r', encoding='utf-8').readlines())

src_file = open('xxx.txt', 'r', encoding='utf-8')
for i in range(1,lines + 1):
    ## 读一行，去除末尾的'\n'
    line = src_file.readline().rstrip()
    ## 奇数行放的是title，偶数行是url
    if i%2 == 0:
        urls = line
        try:
            pdfkit.from_url(urls, titles)
        except Exception as e:
            print(e)
        time.sleep(2)
        # print(titles)
        # print(urls)
    else:
        ## 去掉奇数行的标号
        line = re.sub(r'\d+\. ', '', line)
        line = re.sub(r'[:,?]', '', line)
        ## windows文件命名允许 / ，但是实际上保存文件时出现 / 时会出错。
        line = re.sub(r'/', ' ', line)
        titles = './pdf/' + line + '.pdf'
