import threading
import requests
import os
import time

import urllib3
from fake_useragent import UserAgent

headers = {
    'User-Agent' : str(UserAgent().random)
}

def get_html(url):
    try:
        r = requests.get(url, headers=headers, verify=False)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except Exception as e:
        print(e)

def download_pics(url, n):
    r = get_html(url)
    path = './pic' + str(n) + '.jpg'
    with open(path,'wb') as f:
        f.write(r.content)

urllib3.disable_warnings()
start = time.time()

n = 0
path = './all.txt'
htmlfile = open(path, 'r', encoding='utf-8')
# 需要确定文件夹是否存在
os.chdir('./image/')

for i in htmlfile.readlines():
    i = i.replace('\n','')
    # os.makedirs('./image/')
    n += 1
    print('正在下载第{}张图片'.format(n))
    download_pics(i, n)

end = time.time()
spend = end - start
print('共花费{:.2f}秒'.format(spend))
