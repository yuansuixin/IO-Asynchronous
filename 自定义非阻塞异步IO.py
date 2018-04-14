# -*- coding:UTF-8 -*-
import socket

####################HTTP请求本质，阻塞的#######################
import select


"""
sk = socket.socket()
# 1.链接
sk.connect(('www.baidu.com',80,)) # 阻塞
print('连接成功了。。。')

# 2，链接成功后发送消息
sk.send(b'GET / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\n')
# sk.send(b'POST / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\nk1=v1&k2=v2')
# 3，等待着服务端响应
data = sk.recv(8096)  # 阻塞
print(data)

# 关闭链接
sk.close()
"""

####################HTTP请求本质，非阻塞的#######################
"""
sk = socket.socket()
sk.setblocking(False)
# 1.链接
try:
    sk.connect(('www.baidu.com',80,)) # 阻塞
    print('连接成功了。。。')
except BlockingIOError as e:
    print(e)
# 发送数据就需要连接成功后发送，需要检测着sk是否连接成功，然而这种方法就不好了，那么下面的方法就产生了
# 2，链接成功后发送消息
sk.send(b'GET / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\n')
# sk.send(b'POST / HTTP/1.0\r\nHost:www.baidu.com\r\n\r\nk1=v1&k2=v2')
# 3，等待着服务端响应
data = sk.recv(8096)  # 阻塞
print(data)

# 关闭链接
sk.close()
"""


### Socket客户端的本质
# ### 所有的框架分割请求头和请求体的时候都是使用的split方法

### 封装socket和主机名
class HttpRequest:
    def __init__(self,sk,host,callback):
        self.socket = sk
        self.host = host
        self.callback = callback

    def fileno(self):
        return self.socket.fileno()

class HttpResponse:
    def __init__(self,recv_data):
        self.recv_data = recv_data
        self.header_dict = {}
        self.body= None
        self.initialize()

    def initialize(self):
        # 将请求头和请求题分割
        headers, body = self.recv_data.split(b'\r\n\r\n', 1)
        self.body = body
        headers_list = headers.split(b'\r\n')
        for h in headers_list:
            h_str = str(h,encoding='utf-8')
            v = h_str.split(':',1)
            if len(v) ==2:
                self.header_dict[v[0]] = v[1]


class AsyncRequest():
    def __init__(self):
        self.conn = []
        self.connection = [] # 用于检测是否已经连接成功，有谁，谁就还没有连接成功呢

    def add_request(self,host,callback):
        try:
            sk = socket.socket()
            # 将其变成非阻塞的
            sk.setblocking(0)
            sk.connect((host,80,))
        except BlockingIOError as e:
            pass
        request = HttpRequest(sk,host,callback)
        self.conn.append(request)
        self.connection.append(request)

    def run(self):
        # 事件循环
        while True:
            # IO的多路复用
            rlist,wlist,elist = select.select(self.conn,self.connection,self.conn,0.05)
            #每一个w表示一个HttpRequest对象
            for w in wlist:
                print(w.host,'连接成功')
                # 只要能循环到，表示socket和服务器端已经连接成功
                tp1 = "GET / HTTP/1.0\r\nHost:%s\r\n\r\n"%(w.host)
                # time.sleep(4)
                print(123)
                w.socket.send(bytes(tp1,encoding='utf-8'))
                # 连接只连接一次，成功之后删掉就可以了
                self.connection.remove(w)

            # 接收的数据
            for r in rlist:
                print(r.host, '有数据返回')
                # r是HttpRequest对象
                #  如果有数据就去接收
                recv_data = bytes()
                while True:
                    try:
                        chunk = r.socket.recv(8096)
                        recv_data += chunk
                    except Exception as e:
                        break
                response = HttpResponse(recv_data)
                # 真正用户返回过来的数据
                print(r.host,'返回的数据',recv_data)
                # 对返回的数据进行处理，执行相对应的回调函数
                r.callback(response)
                r.socket.close()
                self.conn.remove(r)

            if len(self.conn) == 0:
                break

def f1(response):
    print('保存文件',response.header_dict)
def f2(response):
    print('保存文件到数据库', response.header_dict)


# 字典格式，每个url对应着他的回调函数

if __name__ == '__main__':
    url_list = [
        {'host': 'www.baidu.com', 'callback': f1},
        {'host': 'cn.bing.com', 'callback': f2},
        # {'host':'www.enblogs.com','callback':f2}
    ]

    req = AsyncRequest()
    for item in url_list:
        req.add_request(item['host'],item['callback'])

    req.run()




























