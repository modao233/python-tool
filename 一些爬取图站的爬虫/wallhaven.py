import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import threading
import os


#设置请求头，随机的
headers= {'User-Agent':str(UserAgent().random)}

#通过生成器返回页面地址
def get_page_url():
    for i in range(50, 60):#最多是(1, 184)
        yield 'https://wallhaven.cc/toplist?page={}'.format(i)

#发送请求，得到页面
def get_html(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except Exception as e:
        print(e)

#存放所有页面Page的壁纸缩略图地址
images = []

#提取每一个page的壁纸缩略图地址，存放进images
def get_href(url):
    res = get_html(url).text
    bsObj = BeautifulSoup(res, "html.parser")
    r = bsObj.select('div#thumbs section.thumb-listing-page ul li figure img')
    for i in r:
        if i['data-src'] not in images:
            images.append(i['data-src'])
        else:
            continue

#下载模块
def download_pics(url, name):
    r = get_html(url)
    path = './' + str(name)
    with open(path,'wb') as f:
        f.write(r.content)
    #下载完了，解锁
    thread_lock.release()

#设置一个简单的计时器
start = time.time()
#转到存放下载文件的目录
os.chdir('D:/python-download/wallhaven/')
#设置最大线程 开启10个线程就锁住
thread_lock = threading.BoundedSemaphore(value=10)

#通过循环获取生成器传出来的值
for i in get_page_url():
    get_href(i)
n = 0

for image in images[:95]:
    #根据转化规则获得真实高清壁纸地址
    author = image.split('/')[-2]
    name = image.split('/')[-1]
    image = 'https://w.wallhaven.cc/full/' + author + '/wallhaven-' + name
    n += 1
    print('正在下载第{}张图片'.format(n))
    # download_pics(image, name)
    # 上锁
    thread_lock.acquire()
    # 下载 这个方法丢进线程池
    t = threading.Thread(target=download_pics, args=(image, name))
    t.start()
    # #time.sleep(0.3)

end = time.time()
spend = end - start
print('共花费{:.2f}秒'.format(spend))