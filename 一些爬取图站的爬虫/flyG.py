import threading

import requests
from bs4 import BeautifulSoup
import os
import time



headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
}

def get_url():
    for i in range(1, 100):
        yield 'http://www.girl13.com/page/{}/'.format(i)

def get_html(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except Exception as e:
        print(e)

images = []

def get_href(url):
    res = get_html(url).text
    bsObj = BeautifulSoup(res, "html.parser")
    r = bsObj.select('div.column-post div a p img')
    for i in r:
        if i['src'] not in images:
            images.append(i['src'])
        else:
            continue

def download_pics(url, n):
    r = get_html(url)
    path = './pic' + str(n) + '.jpg'
    with open(path,'wb') as f:
        f.write(r.content)
    #下载完了，解锁
    thread_lock.release()

start = time.time()
#dir = 'D:/python-download/meizi/'
os.chdir('D:/python-download/flyG/')
#设置最大线程 开启10个线程就锁住
thread_lock = threading.BoundedSemaphore(value=10)
for i in get_url():
    get_href(i)
n = 0
for image in images[:100]:
    n += 1
    print('正在下载第{}张图片'.format(n))
    # 上锁
    thread_lock.acquire()
    # 下载 这个方法丢进线程池
    t = threading.Thread(target=download_pics, args=(image, n))
    t.start()
    #time.sleep(0.3)

end = time.time()
spend = end - start
print('共花费{:.2f}秒'.format(spend))
