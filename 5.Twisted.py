#!/usr/bin/env python
# -*- coding:utf-8 -*-
from twisted.internet import defer
from twisted.web.client import getPage
from twisted.internet import reactor

def one_done(arg):
    print(arg)

def all_done(arg):
    print('done')
    reactor.stop()

@defer.inlineCallbacks
def task(url):
    res = getPage(bytes(url, encoding='utf8')) # 发送Http请求
    res.addCallback(one_done)
    yield res

url_list = [
    'http://www.cnblogs.com',
    'http://www.cnblogs.com',
    'http://www.cnblogs.com',
    'http://www.cnblogs.com',
]

defer_list = [] # [特殊，特殊，特殊(已经向url发送请求)],都是defer对象
## 对URl进行循环，拿到一个url就执行task任务，发送Http请求，发完请求就返回，已经向url发送完请求的特殊对象
# 将这些特殊对象添加到defer_list列表中，将这个列表传入DeferredList对象中，那么这些特殊的对象就成了defer对象，
# 这些请求每返回一个请求就会执行一次one_done方法，同时reactor.run()死循环一直在检测是否所有请求都返回了，这里做了请求返回数量统计，如果所有的请求都返回了，
# #执行all_done方法，将reactor死循环结束


for url in url_list:
    v = task(url)
    defer_list.append(v)

d = defer.DeferredList(defer_list)
d.addBoth(all_done)
reactor.run() # 死循环