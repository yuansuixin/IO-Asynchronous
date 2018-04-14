# -*- coding:UTF-8 -*-



'''
可以实现并发
但是，请求发送出去和返回之前，中间时期线程空闲

'''


########### 编写方式一################
'''
from concurrent.futures import ThreadPoolExecutor
import requests

def task(url):
    response = requests.get(url)
    print(url,response)
    # 处理返回值
    # 写正则


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
    pool.submit(task,url)
    
pool.shutdown(wait=True)
'''

########### 编写方式二################

from concurrent.futures import ThreadPoolExecutor
import requests

def task(url):
    '''
    只下载页面
    :param url:
    :return:
    '''
    response = requests.get(url)
    print(url,response)

def done(future,*args,**kwargs):
    '''
    请求成功之后，执行的回调函数，处理一些东西
    与编写方式一来说，降低了耦合度
    :param future:
    :param args:
    :param kwargs:
    :return:
    '''
    print(future,args,kwargs)
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












