from selenium import webdriver
import time
import json
import random
import requests
import re

# 填写公众号登录信息
account_name = 'xxx'
password = 'xxx'

#登录微信公众号，获取cookie，保存到本地文本
def wechat_login():
    #用webdriver启动火狐
    #修改火狐安装路径
    driver = webdriver.Firefox(firefox_binary='D:/Mozilla Firefox/firefox.exe')
    driver.get('http://mp.weixin.qq.com/')
    time.sleep(2)

    #清空账号框的内容
    driver.find_element_by_name('account').clear()
    driver.find_element_by_name('account').send_keys(account_name)
    time.sleep(2)
    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys(password)
    time.sleep(3)

    #在自动输入账号密码后手动点击记住我
    print('请在登录界面点击：记住账号')
    driver.find_element_by_class_name('frm_checkbox_label').click()
    time.sleep(5)

    #自动点击登录按钮进行登录
    driver.find_element_by_class_name('btn_login').click()

    #手机扫描二维码
    print('用手机扫描二维码')
    time.sleep(15)
    print('登录成功')
    cookie_items = driver.get_cookies()
    post = {}

    #获取到的cookies是列表形式，转化成json形式并存入本地名为cookie的文本中
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    with open('cookie.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    print('cookie保存成功')
    f.close()
    driver.quit()

#爬取公众号文章，保存在本地文本中
def get_content(query):
    
    url = 'https://mp.weixin.qq.com'

    header = {
        'HOST': 'mp.weixin.qq.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)

    #增加重试连接次数
    session = requests.Session()
    session.keep_alive = False

    session.adapters.DEFAULT_RETRIES = 511
    time.sleep(5)

    response = session.get(url=url, cookies=cookies, verify=False)

    token = re.findall(r'token=(\d+)', str(response.url))[0]
    time.sleep(2)

    #搜索公众号的接口地址
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'

    #搜索微信公众号接口需要传入的参数，有三个变量：微信公众号的token， 随机数random， 搜索的微信公众号的名字
    query_id = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f':'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '0',
        'count': '5'
    }
    #打开微信公众号的接口地址，传入参数
    search_response = session.get(
        search_url,
        cookies=cookies,
        headers = header,
        params = query_id
    )
    #获取搜索结果中的第一个公众号
    lists = search_response.json().get('list')[0]
    print(lists)
    #获取这个公众号的fikeid
    fakeid = lists.get('fakeid')

    #公众号文章接口地址
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'

    #搜索公众号需要传入几个参数
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    #打开搜索的微信公众号文章列表
    appmsg_response = session.get(
        appmsg_url,
        cookies=cookies,
        headers=header,
        params = query_id_data
    )
    max_num = appmsg_response.json().get('app_msg_cnt')
    #设置分页
    num = int(int(max_num)/5) + 1
    begin = 0
    seq = 0
    while num  > 0:
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        print('正在翻页：---------------------', begin)
        time.sleep(5)

        #获取每一页文章的标题和链接地址，并写入本地文本中
        query_fakeid_response = requests.get(
            appmsg_url,
            cookies = cookies,
            headers = header,
            params = query_id_data
        )
        fakeid_list = query_fakeid_response.json().get('app_msg_list')
        if fakeid_list:
            for item in fakeid_list:
                content_link = item.get('link')
                content_title = item.get('title')
                fileNamq = query + '.txt'
                seq += 1
                with open(fileNamq, 'a', encoding='utf-8') as f:
                    f.write(str(seq) + ". " + content_title + "\n"+ content_link + '\n')
        num -= 1
        begin = int(begin)
        begin += 5

wechat_login()
#query为要爬取的公众号的名称
query = 'xxx'
print('开始爬取公众号')
get_content(query)
print('爬取完成')