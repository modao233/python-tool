import json
import time
from fake_useragent import UserAgent
import requests
import random

headers = {
    'User-Agent' : str(UserAgent().random)
}

def get(url):
    page = requests.get("http://144.34.226.152:5010/get/").content.decode('utf-8')
    page = json.loads(page)
    pro = page['proxy']
    p = {'http': "http://{}".format(pro)}
    page = requests.get(url, headers=headers, proxies=p)
    time.sleep(random.randint(2,3))

for i in range(10):
    get("https://mp.weixin.qq.com/s?__biz=MzIyMjMwNzgyMw==&mid=100000012&idx=1&sn=72bd6cae5f4a52e4cbe986d7ca5acbad&chksm=682e358c5f59bc9ac098c6263ec1c6dba22a4821bca8c4c9ef14fb8bf241c145233b5ae21709&scene=18&xtrack=1&key=c8b1cdfc5f2a0a52611626b12bdd44f83087c866323a9197621e11c5c09850b72d769ea7f76dba5a99899ecf16c38a0ec0bc8ac45641574a6a1b366475e3bee9c03fa2c841530109c74e08550b617796&ascene=1&uin=Mjg1NjY4NTkxMQ%3D%3D&devicetype=Windows+10&version=62060834&lang=zh_CN&pass_ticket=lu1elIHosSU0kzvoP7aTs1kH0WByfeLQyAGgwu018Ar3R6Z7YaEGGAKh%2F%2FaK1t%2Bh")