# -*- coding:UTF-8 -*-

import gevent

import requests
from gevent import monkey

# 找到socket然后封装gevent专门提供的并发，才可以实现并发
monkey.patch_all()


def fetch_async(method, url, req_kwargs):
    print(method, url, req_kwargs)
    response = requests.request(method=method, url=url, **req_kwargs)
    print(response.url, response.content)

# ##### 发送请求 #####
gevent.joinall([
    gevent.spawn(fetch_async, method='get', url='https://www.python.org/', req_kwargs={}),
    gevent.spawn(fetch_async, method='get', url='https://www.yahoo.com/', req_kwargs={}),
    gevent.spawn(fetch_async, method='get', url='https://github.com/', req_kwargs={}),
])

# ##### 发送请求（协程池控制最大协程数量） #####
# from gevent.pool import Pool
# 在None的地方填入具体的值，最多能发None个
# pool = Pool(None)
# gevent.joinall([
#     pool.spawn(fetch_async, method='get', url='https://www.python.org/', req_kwargs={}),
#     pool.spawn(fetch_async, method='get', url='https://www.yahoo.com/', req_kwargs={}),
#     pool.spawn(fetch_async, method='get', url='https://www.github.com/', req_kwargs={}),
# ])














