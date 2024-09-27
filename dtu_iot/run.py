#!/usr/bin/python3
import json

from dtu_iot import dtu_simulation

# 功能码03保持寄存器 -数据类型int16
# 功能码02输入状态-数据类型bit
# 功能码01线圈状态-数据类型bit
if __name__ == '__main__':
    address = '[{"ip":"10.4.142.210","port":22602,"login_payload":"HL01T_98765412389000","heartbeat_time":30}]'
    for data in json.loads(address):
        dtu = dtu_simulation.DtuSimulation(data["ip"], data["port"], data["login_payload"], data["heartbeat_time"])
        dtu.client(rand=True)
