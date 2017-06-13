# -*- coding: utf-8 -*-：
import socket
import os
import struct
import threading
import time
from ctypes import *
from netaddr import IPAddress,IPNetwork

host = "172.16.144.25"

#扫描的子网
subnet = "172.0.0.0 /8"

#自定义到字符串,我们将在ICMP响应中核对
magic_message = "PYTHONRULES!"

def udp_sender(subnet,magic_message):
    time.sleep(1)
    sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message,("%s" % ip,65212))

        except:
            pass



class IP(Structure):
    _fields_ = [
        ("ihl",             c_ubyte, 4),
        ("version",         c_ubyte, 4),
        ("tos",             c_ubyte),
        ("len",             c_ushort),
        ("id",              c_ushort),
        ("offset",          c_ushort),
        ("ttl",             c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum",             c_ushort),
        ("src",             c_uint32),
        ("dst",             c_uint32),

    ]

    def __new__(self,socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self,socket_buffer=None):
        #协议字段于协议名称对应
        self.protocol_map = {1:"ICMP",6:"TCP",17:"UDP"}

        #可读性过更强到IP地址
        self.src_address = socket.inet_ntoa(struct.pack("@I",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))

        #协议类型
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    _fields_ = [
        ("type",            c_ubyte),
        ("code",            c_ubyte),
        ("checksum",        c_ushort),
        ("unused",          c_ushort),
        ("next_hop_mtu",    c_ushort)
    ]

    def __new__(self,socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self,socket_buffer):
       pass

if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)

sniffer.bind((host,0))

sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
t.start()

try:
    while True:
        #读取数据包
        raw_buffer = sniffer.recvfrom(65565)[0]

        #将缓冲区到前20个字符按IP头进行解析
        ip_header = IP(raw_buffer[0:20])
        #输出协议和通讯双方IP地址
        #print "Protocol: %s %s -> %s" %(ip_header.protocol,ip_header.src_address,ip_header.dst_address)
        if ip_header.protocol == "ICMP":
            #计算IMCP包到起始位置
            offset = ip_header.ihl * 4;
            buf = raw_buffer[offset:offset + sizeof(ICMP)]
            #解析ICMP数据
            icmp_header = ICMP(buf)
            #print "ICMP -> Type: %d Code:%d" %(icmp_header.type,icmp_header.code)
            if icmp_header.code == 3 and icmp_header.type == 3:

                if IPAddress(ip_header.src_address ) in IPNetwork(subnet):


                        print "Host Up:%s "%ip_header.src_address

except  KeyboardInterrupt:
    # 如果运行再Windows上,关闭混杂模式
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

