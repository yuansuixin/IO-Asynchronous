
> # 并发

### 同步执行

```
import requests

def fetch_async(url):
    response = requests.get(url)
    return response


url_list = ['http://www.github.com', 'http://www.bing.com']

for url in url_list:
    fetch_async(url)
```

### 多线程实现并发
   - 两种编写形式
    1. 请求和处理放在一起
    2. 请求和处理分开，请求成功后执行回调函数，降低了耦合性

```

'''
可以实现并发
但是，请求发送出去和返回之前，中间时期线程空闲

'''

########### 编写方式一################
'''
from concurrent.futures import ThreadPoolExecutor
import requests

def task(url):
 response = requests.get(url) print(url,response) # 处理返回值 # 写正则

pool = ThreadPoolExecutor(7)
url_list = [
 'https://www.baidu.com/', 'https://www.sina.com/', 'https://www.zhihu.com/', 'https://www.autohome.com/', 'https://www.bing.com/', 'https://www.csdn.net/', 'https://www.oschina.net/',
]

for url in url_list:
 pool.submit(task,url) pool.shutdown(wait=True)
'''

########### 编写方式二 回调函数################

from concurrent.futures import ThreadPoolExecutor
import requests

def task(url):
    '''
 只下载页面  :param url:  :return:
 '''  response = requests.get(url)
    print(url,response)

def done(future,*args,**kwargs):
    '''
 请求成功之后，执行的回调函数，处理一些东西 与编写方式一来说，降低了耦合度  :param future:  :param args:  :param kwargs:  :return:
 '''  print(future,args,kwargs)
    print(future.result,args,kwargs)
    response = future.result()
    print(response.status_code,response.content)

pool = ThreadPoolExecutor(7)
url_list = [
    'https://www.baidu.com/',
    'https://www.sina.com/',
    'https://www.zhihu.com/',
    'https://www.autohome.com/',
    'https://www.bing.com/',
    'https://www.csdn.net/',
    'https://www.oschina.net/',

]

for url in url_list:
    v= pool.submit(task,url)
    # 执行回调函数，可以有多个回调
  v.add_done_callback(done)

pool.shutdown(wait=True)

```


### 多进程实现并发

```

'''
可以实现并发
但是，请求发送出去和返回之前，中间时期线程空闲
'''

########### 编写方式一################
'''
from concurrent.futures import ProcessPoolExecutor
import requests

def task(url):
 response = requests.get(url) print(url,response) # 处理返回值 # 写正则

pool = ProcessPoolExecutor(7)
url_list = [
 'https://www.baidu.com/', 'https://www.sina.com/', 'https://www.zhihu.com/', 'https://www.autohome.com/', 'https://www.bing.com/', 'https://www.csdn.net/', 'https://www.oschina.net/',
]

for url in url_list:
 pool.submit(task,url) pool.shutdown(wait=True)
'''

########### 编写方式二  回调函数################

from concurrent.futures import ProcessPoolExecutor
import requests

def task(url):
    '''
 只下载页面  :param url:  :return:
 '''  response = requests.get(url)
    print(url,response)

def done(future,*args,**kwargs):
    '''
 请求成功之后，执行的回调函数，处理一些东西 与编写方式一来说，降低了耦合度  :param future:  :param args:  :param kwargs:  :return:
 '''  print(future,args,kwargs)
    print(future.result,args,kwargs)
    response = future.result()
    print(response.status_code,response.content)

pool = ProcessPoolExecutor(7)
url_list = [
    'https://www.baidu.com/',
    'https://www.sina.com/',
    'https://www.zhihu.com/',
    'https://www.autohome.com/',
    'https://www.bing.com/',
    'https://www.csdn.net/',
    'https://www.oschina.net/',

]

for url in url_list:
    v= pool.submit(task,url)
    # 执行回调函数，可以有多个回调
  v.add_done_callback(done)

pool.shutdown(wait=True)

```

> # 多线程和多进程的区别

- 多线程 IO密集型，不用通过cpu
- 多进程 计算密集型

[多线程和多进程的区别和联系](https://yuansuixin.github.io/2017/04/14/much-thread/ "多线程和多进程的区别和联系")

> # 异步IO

### 协程（微线程）
    - 协程能完成切换，什么时候切换得需要咱们自己设
    - 加上http请求的话，就是请求回来之后切换
    - 加上异步IO的功能就等同于一个线程发送N个http请求，asyncio可以帮助我们完成这个操作

> # asyncio

### TCP
    - 使用socket实现
    ​```
    client = socket()
    client.connect(...)
    client.send(b'ffdsafdsa')
    ​```
### HTTP
    - HTTP是基于TCP做的
    - 也是使用socket实现
    
    ​```
    #http是基于tcp的，只不过发送的数据不一样，http有固定的数据格式
    data = "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n"
    client = socket()
    client.connect(...)
    client.send(data)
    ​```

### 原理

>> #### 角色 ：使用者

   - asyncio.sleep(5) 等待

``` python
import asyncio

@asyncio.coroutine
def task():
    print('before ....task')
    yield from asyncio.sleep(5)
    # 发送http请求，但是asyncio只支持TCP获取结果，那么我们就需要自己弄成http请求
    print('end ....task')


tasks = [task(),task()]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()

```


   - 自己封装Http数据包

```
import asyncio

###自己封装http的数据包
@asyncio.coroutine
def task(host, url='/'):
    print(host, url)
    # 创建链接
    reader, writer = yield from asyncio.open_connection(host, 80)

    # http请求的格式
    request_header_content = """GET %s HTTP/1.0\r\nHost: %s\r\n\r\n""" % (url, host,)
    request_header_content = bytes(request_header_content, encoding='utf-8')

    writer.write(request_header_content)
    yield from writer.drain()
    text = yield from reader.read()
    print(host, url, text)
    writer.close()

tasks = [
    task('www.cnblogs.com', '/wupeiqi/'),
    task('dig.chouti.com', '/pic/show?nid=4073644713430508&lid=10273091')
]

loop = asyncio.get_event_loop()
results = loop.run_until_complete(asyncio.gather(*tasks))
loop.close()

```
   - aiohttp模块，封装了Http数据包，这个包需要下载，

```
import aiohttp
import asyncio


@asyncio.coroutine
def fetch_async(url):
    print(url)
    response = yield from aiohttp.request('GET', url)
    # data = yield from response.read()
    # print(url, data)
    print(url, response)
    response.close()


tasks = [fetch_async('http://www.baidu.com/'), fetch_async('http://www.chouti.com/')]

event_loop = asyncio.get_event_loop()
results = event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()
```

   - requests模块，封装了Http数据包，也是需要下载的

```
import asyncio
import requests


@asyncio.coroutine
def task(func, *args):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, func, *args)
    response = yield from future
    print(response.url, response.content)


tasks = [
    task(requests.get, 'http://www.cnblogs.com/wupeiqi/'),
    task(requests.get, 'http://dig.chouti.com/pic/show?nid=4073644713430508&lid=10273091')
]

loop = asyncio.get_event_loop()
results = loop.run_until_complete(asyncio.gather(*tasks))
loop.close()
```

> # gevent

- 和asyncio的本质原理一致，实现方式不同，依赖了协程的greenlet模块，和异步IO的结合
- 需要安装greenlet，gevent

- gevent+requests模块
- gevent(协程池，最多发多少个请求)+requests模块 

```
import gevent

import requests
from gevent import monkey

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
# pool = Pool(None)
# gevent.joinall([
#     pool.spawn(fetch_async, method='get', url='https://www.python.org/', req_kwargs={}),
#     pool.spawn(fetch_async, method='get', url='https://www.yahoo.com/', req_kwargs={}),
#     pool.spawn(fetch_async, method='get', url='https://www.github.com/', req_kwargs={}),
# ])
```


- gevent+requests==》 grequests 模块，需要下载，其实原理就是gevent和requests的原理，只不过做了个封装而已

```
import grequests


request_list = [
    grequests.get('http://httpbin.org/delay/1', timeout=0.001),
    grequests.get('http://fakedomain/'),
    grequests.get('http://httpbin.org/status/500')
]


# ##### 执行并获取响应列表 #####
# response_list = grequests.map(request_list)
# print(response_list)


# ##### 执行并获取响应列表（处理异常） #####
# def exception_handler(request, exception):
# print(request,exception)
#     print("Request failed")

# response_list = grequests.map(request_list, exception_handler=exception_handler)
# print(response_list)
```

> # Twisted

- scarpy框架底层使用的Twisted实现的

```
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
```



> # tonado

```
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado import ioloop

COUNT = 0
def handle_response(response):
    global COUNT
    COUNT -= 1
    if response.error:
        print("Error:", response.error)
    else:
        print(response.body)
        # 方法同twisted
        # ioloop.IOLoop.current().stop()
    if COUNT == 0:
        ioloop.IOLoop.current().stop()

def func():
    url_list = [
        'http://www.baidu.com',
        'http://www.bing.com',
    ]
    global COUNT
    COUNT = len(url_list)
    for url in url_list:
        print(url)
        http_client = AsyncHTTPClient()
        http_client.fetch(HTTPRequest(url), handle_response)


ioloop.IOLoop.current().add_callback(func)
ioloop.IOLoop.current().start() # 死循环
```


#### 使用哪个最好呢，一般都是直接使用的框架，人家已经帮我们封装好了，如果是需要自己写，=======》gevent >  Twisted  >   Tornado  > asyncio

以上均是Python内置以及第三方模块提供异步IO请求模块，使用简便大大提高效率，而对于异步IO请求的本质则是【非阻塞Socket】+【IO多路复用】


>>  #### 角色： NB开发者

### 学习自定义异步IO框架必备知识点
###### 1. socket客户端，服务端
    - 连接是阻塞的，receive也会阻塞
    - setblocking(0)的话连接就不会阻塞了，无数据（连接无响应，数据未返回）就报错
    - 不管阻塞或者是非阻塞，连接都会发到远程，阻塞的话就会等，等着连接回来

###### 2. IO多路复用
     - 客户端

```
try:
   socket对象1.connet（）
   socket对象2.connet（）
   socket对象3.connet（）
except EX...
    pass

while True:
# 监听对象
    r,w,e = select.select([socket对象，socket对象。。。],[socket对象，socket对象。。。],[],0.05)
    e 表示多路复用发生异常，错误就会放到e里面
    # 表示有人给我发送数据
    r = [socket对象1，]
       xx = socket对象1.recv()
    # 表示我已经和别人创建链接成功
    w = [socket对象1，]
        socket对象1.send('GET %s HTTP/1.0\r\nHost: %s\r\n\r\n')
```

###### 3.
- select.select监听对象的内部并不是只能有socket对象，但是必须有，fileno方法，并且返回一个文件描述符
    - select内部：对象.fileno()
    - Foo（）内部封装socket文件描述符

```
class Foo:
    def fileno(self):
        obj = socket()
        return obj.fileno()

#这个对象必须有：fileno方法，并返回一个文件描述符
    r,w,e = select.select([对象，对象。。。],[对象，对象。。。],[],0.05)
```


### 自定义异步IO框架

- Http请求的本质，阻塞的
- Http请求的本质，非阻塞的
- 非阻塞异步IO框架

[自定义非阻塞异步IO详细讲解](https://yuansuixin.github.io/2018/04/14/io-asynchronous/ "详细讲解")


- 什么是异步IO
    - 异步IO是相对来说的，如果有人来用的话，只需要给url和回调函数就可以，请求完成之后，会自动调用回调函数，对于使用的人来说就是异步，其实就是回调
    - 对于开发者来说，就不是异步的
    - select仅仅是IO多路复用，只能同时监听多个对象，他自己完成不了，不能实现异步，只能监听对象，谁又变化就记录下来，利用其特性可以开发出异步IO模块
    - 异步IO  （非阻塞的socket+IO多路复用就可以开发出）
        - 异步的IO请求，当有多个请求的时候，可以做多个事情，而不是一直等着，请求返回时自动调用回调函数
          -（单个线程伪造了好多请求发过去，多并发）
        - socket非阻塞
        - select监听的时候，可以封装成自己的对象








