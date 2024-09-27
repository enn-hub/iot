#!/usr/bin/python3


import crcmod

from logger import logger


# 参数组装
def parameter_assembly(value, resp):
    function_code, address_code = message_parsing(resp)
    value = decimal_conversion(value)
    if function_code in ("01", "02", "03", "04"):
        code = function_code
    else:
        code = "03"
    if code == "03" or code == "04":
        length = '0200'  # 第4、5位 *2 转16进制
        # crc = crc_data(address + code + length + value)
        # param = address + code + length + value + crc
    elif code == "01" or code == "02":
        length = '01'
    crc = crc_data(address_code + code + length + value)
    param = address_code + code + length + value + crc
    logger.info(msg="[+]当前请求的value值：%s" % value)
    # logger.info(msg="[+]开始组装参数，结果：%s" % param)
    return param


def message_parsing(resp):
    function_code_data = bytes([resp[1]])
    function_code = '{:02x}'.format(function_code_data[0])
    address_code_data = bytes([resp[0]])
    address_code = '{:02x}'.format(address_code_data[0])
    return function_code, address_code


# 数制转换
def decimal_conversion(decimal_num):
    # 将10进制数转换成16进制字符串
    if decimal_num < 10:
        hex_str = '{:02d}'.format(decimal_num)
    else:
        hex_str = hex(decimal_num)
    # 输出16进制字符串
    return hex_str[2:]


# 生成crc校验码
def crc_data(data):
    result_datas = None
    # logger.info(msg="[+]开始生成crc校验码，原始数据：%s" % data)
    try:
        # 将十六进制字符串转换成二进制数据
        data_bytes = bytes.fromhex(data)
        # 计算CRC校验码
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        crc = crc16(data_bytes)
        # 将CRC校验码转换成字节序列
        convert_data = crc.to_bytes(length=2, byteorder='big')
        result_datas = convert_data[::-1]
        # 输出结果
        logger.info(msg="[+]开始生成crc校验码，结果：%s" % result_datas.hex())
    except Exception as e:
        logger.error(msg="[-]crc校验码生成失败，数据：%s 异常：%s" % (data, e))
    return result_datas.hex()


if __name__ == "__main__":
    print(crc_data('02010100'))
    # parameter_assembly('01',100)
