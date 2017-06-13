# -*- coding:utf-8 -*-
import socket
import threading
import json
import MySQLdb

# data = """
# {
#     "states": "",
#     "data":
#         {
#             "time": "11",
#             "temperature": "",
#             "humidity": ""
#         }
#
# }
# """
# d1 = json.loads(data)
# data = d1["data"]["time"]
# print data

# 数据库连接
coon = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='raspberry_pi'
)

cur = coon.cursor()
select_sql = "select * from dnt11 order by _id desc limit 0,5"
count = cur.execute(select_sql)

bind_ip = "10.9.34.94"
bind_port = 8081
insert_sql = "insert into dnt11(times,temperature,humidity) VALUES (%s,%s,%s)"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)


# 解析Json
def jsonToStr(strJson):
    strJson = json.loads(strJson)
    time = strJson["data"]["time"]
    temperature = strJson["data"]["temperature"]
    humidity = strJson["data"]["humidity"]

    return time, temperature, humidity


# 读取传感器 拼接最新5条数据
def sqlToJson():
    items = cur.fetchall()

    data = '{"states": "1","data":['
    for i in range(count):
        data += '{'
        data += '"time":"' + items[i][1] + '",'
        data += '"temperature":"' + items[i][2] + '",'
        data += '"humidity":"' + items[i][3] + '"'
        data += '}'
        if i != count:
            data += ','

    data += ']}'

    return data


def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)

        strJson = json.loads(request)
        states = strJson["states"]
        print type(states)
        if states == '0':
            time, temperature, humidity = jsonToStr(request)
            print time, temperature, humidity
            cur.execute(insert_sql, (time, temperature, humidity))
            coon.commit()

        elif states == '1':
            data = sqlToJson()
            client_socket.send(data)

        elif states == 'w':

        elif states == 'a':

        elif states == 's':

        elif states == 'd':

        elif states == 'x':


        # client_socket.send("ACK!")



while True:
    client, addr = server.accept()
    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

"""
{
    "states": "",
    "data": [
        {
            "time": "",
            "temperature": "",
            "humidity": ""
        }
    ]
}
"""
