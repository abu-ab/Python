# -*- coding: utf-8 -*-：
import MySQLdb
import socket

coon = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='raspberry_pi',
    charset='utf8'
)

cur = coon.cursor()

# 开启ip和端口
ip_port = ('10.9.37.188', 8801)
# 生成句柄
web = socket.socket()
# 绑定端口
web.bind(ip_port)
# 最多连接数
web.listen(5)
# 等待信息
print ('nginx waiting...')
# 开启死循环
while True:
    # 阻塞
    conn, addr = web.accept()
    # 获取客户端请求数据
    data = conn.recv(1024)
    # 打印接受数据 注：当浏览器访问的时候，接受的数据的浏览器的信息等。
    print(data)
    # 向对方发送数据
    conn.send(bytes('<h1>welcome nginx</h1>'))
    # 关闭链接
    conn.close()
