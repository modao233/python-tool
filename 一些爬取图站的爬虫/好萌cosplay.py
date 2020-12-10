import threading

import requests
from bs4 import BeautifulSoup
import os
import time
import urllib3




from fake_useragent import UserAgent

headers = {
    'User-Agent' : str(UserAgent().random)
}

def get_url():
    for i in range(13, 20):
        yield 'https://nicemoe2.com/picture/cosplay/page/{}/'.format(i)

def get_html(url):
    try:
        r = requests.get(url, headers=headers, verify=False)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except Exception as e:
        print(e)

images = []


def get_href(url):
    res = get_html(url).text
    bsObj = BeautifulSoup(res, "html.parser")
    #r = bsObj.xpath('/html/body/div[5]/div[2]/article[54]/div/a')
    r = bsObj.select('div.inn-archive__item__container.inn-card_painting__item__container a')
    for i in r:
        if i['href'] not in images:
            images.append(i['href'])
        else:
            continue


def get_img(url):
    res = get_html(url).text
    bsObj = BeautifulSoup(res, "html.parser")
    #r = bsObj.xpath('/html/body/div[5]/div[2]/article[54]/div/a')
    r = bsObj.select('div.inn-singular__post__body__content.inn-content-reseter p img')
    for i in r:
        if i['src'] not in img:
            img.append(i['src'])
        else:
            continue


def download_pics(url, n):
    r = get_html(url)
    path = './pic' + str(n) + '.jpg'
    with open(path,'wb') as f:
        f.write(r.content)


urllib3.disable_warnings()
start = time.time()
#dir = 'D:/python-download/meizi/'
# os.chdir('D:/python-download/cos/')
#设置最大线程 开启10个线程就锁住
thread_lock = threading.BoundedSemaphore(value=10)
for i in get_url():
    get_href(i)

n = 0

for i in images:
    # 上锁
    thread_lock.acquire()

    os.chdir('D:/python-download/cos/')
    img = []
    file = i.split('/')[-2]
    isExists = os.path.exists(file)
    if not isExists:
        os.makedirs(file)
    os.chdir('D:/python-download/cos/'+file)
    get_img(i)

    for image in img:
        n += 1
        print('正在下载第{}张图片'.format(n))
        # download_pics(image, n)

        # 下载 这个方法丢进线程池
        t = threading.Thread(target=download_pics, args=(image, n))
        t.start()
        #time.sleep(0.3)

    # 下载完了，解锁
    thread_lock.release()

end = time.time()
spend = end - start
print('共花费{:.2f}秒'.format(spend))
