#!/usr/bin/python3
# --*-- coding: utf-8 --*--
import logging

# 创建日志记录器
logger = logging.getLogger()

# 配置日志记录器的级别
logger.setLevel(logging.INFO)

# 创建控制台日志处理器,Handler 将日志信息发送到设置的位置
handler = logging.StreamHandler()

# 配置日志处理器的格式
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',  # 这里需要在当前文件的同一目录下自己去创建一个myapp.log的文件
                    filemode='w')

# 将日志处理器添加到日志记录器中
logger.addHandler(handler)
