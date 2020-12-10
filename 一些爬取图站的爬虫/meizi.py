import requests
from bs4 import BeautifulSoup
import os
import time



headers = {
'Referer':'https://www.mzitu.com/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
}

def get_url():
    for i in range(1, 10):
        yield 'https://www.mzitu.com/page/{}/'.format(i)

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
    r = bsObj.select('div.postlist ul#pins li a')
    for i in r:
        if i['href'] not in images:
            images.append(i['href'])
        else:
            continue

start = time.time()
#dir = 'D:/python-download/meizi/'
os.chdir('D:/python-download/meizi/')

for i in get_url():
    get_href(i)

for image in images[:100]:
    res = get_html(image).text
    bsObj = BeautifulSoup(res, "html.parser")
    count = bsObj.select('div.content div.pagenavi a')[-2].string

    for c in range(1, int(count) + 1):
        url = image + '/' + str(c)
        response = get_html(url).text
        bsObj2 = BeautifulSoup(response, 'html.parser')
        for src in bsObj2.select('div.main-image p a img'):
            src = src['src']
            file = url.split('/')[-2]
            content = get_html(src)
            isExists = os.path.exists(file)
            if not isExists:
                os.makedirs(file)
            path = src.split('/')[-1]
            with open(file+'/'+path, 'wb') as f:
                f.write(content.content)
            f.close()
            print(src)
            time.sleep(0.3)

end = time.time()
spend = end - start
print('共花费{:.2f}秒'.format(spend))
