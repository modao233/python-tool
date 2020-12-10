import json
import time
from fake_useragent import UserAgent
import requests
import threading
import os

headers= {'User-Agent':str(UserAgent().random)}
# #设置最大线程 开启10个线程就锁住
# thread_lock = threading.BoundedSemaphore(value=10)

#返回图片URL所在页面
def get_url(id, photo_count):
    for i in range(1,3):
        url = ""
        if (id == 1):
            url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c68ffb9463b7fbfe72b0db0?page={}&per_page='.format(i) + str(
                photo_count)
        elif (id == 2):
            url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c69251c9b1c011c41bb97be?page={}&per_page='.format(i) + str(
                photo_count)
        elif (id == 3):
            url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c81087e6aee28c541eefc26?page={}&per_page='.format(i) + str(
                photo_count)
        elif (id == 4):
            url = 'https://service.paper.meiyuan.in/api/v2/columns/flow/5c81f64c96fad8fe211f5367?page={}&per_page='.format(i) + str(
                photo_count)
        yield url
#通过url 获取数据
#单个页面
def get_page(url):
    #requests.get 自带了json.loads(假的)
    page = requests.get(url, headers=headers)
    #提取需要的content
    page = page.content
    # 对json格式转化为python对象
    page = json.loads(page)
    return page

#筛选图片URL
def pic_urls_from_pages(pages):
    pic_urls = []
    for page in pages:
        # 处理一个页面
        url = page['urls']
        if url['raw'] not in pic_urls:
            pic_urls.append(url['raw'])
    return pic_urls

#下载模块：从URL下载并保存图片
def download_pics(url, n):
    r = requests.get(url)
    path = './pic' + str(n) + '.jpg'
    with open(path,'wb') as f:
        f.write(r.content)
    # #下载完了，解锁
    # thread_lock.release()


def main(id, photo_count):
    n = 0
    for i in get_url(id, photo_count):
        page = get_page(i)
        pic_urls = pic_urls_from_pages(page)

        for url in pic_urls:
            n += 1
            print('正在下载第{}张图片'.format(n))
            download_pics(url, n)
            # # 上锁
            # thread_lock.acquire()
            # # 下载 这个方法丢进线程池
            # t = threading.Thread(target=download_pics, args=(url, n))
            # t.start()


os.chdir('D:/python-download/wallpaper/1/')
main(4, 20)