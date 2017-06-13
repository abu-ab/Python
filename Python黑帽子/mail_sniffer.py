# -*- coding: utf-8 -*-：

from scapy.all import *

# 数据包回调函数
def packet_callback(packet):
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)

        if "username" in mail_packet.lower() or "password" in mail_packet.lower():
            print "[*] Server: %s " %packet[IP].dst
            print "[*] %s " % packet[TCP].payload


# 开启嗅探器
sniff(filter="tcp port 88 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)

