#!/usr/bin/python3

import binascii
import random
import socket
import threading
import time

from dtu_iot import dtu_param
from logger import logger


class DtuSimulation:

    def __init__(self, ip, port, login_payload, heartbeat_time):
        self.ip = ip
        self.port = port
        self.login_payload = login_payload
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)  # socket.AF_INET是ipv4的地址家族socket.SO_MARK的使用是TCP协议 调用socket中socket()来创建一个socket
        self.heartbeat_time = heartbeat_time

    def client(self, value=None, rand=False):
        self.socket.connect((self.ip, self.port))
        logger.info(msg="%s 开始连接网关：%s %s" % (self.login_payload, self.ip, self.port))
        logger.info(msg="发送认证报文：%s " % self.login_payload)
        self.socket.send(self.login_payload.encode())
        data = self.socket.recv(1024)
        logger.info(msg="%s认证成功，响应报文data：%s" % (self.login_payload, data))
        if self.heartbeat_time != 0:
            t1 = threading.Thread(target=self.send_heartbeat)
            t1.start()
        t2 = threading.Thread(target=self.send_data, args=(value, rand, data))
        t2.start()

    def send_heartbeat(self):
        while True:
            logger.info(msg="发送心跳报文：%s " % self.login_payload)
            self.socket.send(self.login_payload.encode())
            time.sleep(self.heartbeat_time)

    def send_data(self, value, rand, data):
        while data:
            if rand:
                num = random.randint(16, 99)
                logger.info(msg="%s 报文value：%s " % (self.login_payload, num))
                param = dtu_param.parameter_assembly(num, data)
            else:
                param = dtu_param.parameter_assembly(value, data)
            logger.info("%s发送数据报文：%s" % (self.login_payload, param))
            self.socket.sendall(binascii.unhexlify(param))
            data = self.socket.recv(1024)
            logger.info(msg="数据响应报文：%s " % data)
