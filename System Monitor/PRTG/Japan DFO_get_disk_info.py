#!..\..\redist\Python34
# -*- coding: utf-8 -*-

from paepy.ChannelDefinition import CustomSensorResult
import sys
import json
import pymssql
import datetime
deviceID = 12
if __name__ == "__main__":
    conn = pymssql.connect(server='10.0.0.55', user='DFO_Trial', password='DynaCW999', database='SystemMonitor')
    cursor = conn.cursor()
    endDate = datetime.datetime.now()
    startDate = endDate - datetime.timedelta(0, 180)
    cursor.execute("SELECT * FROM DeviceInfo WHERE DeviceID = '" + str(deviceID) + "' AND UpdateTime BETWEEN '" + startDate.strftime("%Y/%m/%d %H:%M:%S") + "' AND '" + endDate.strftime("%Y/%m/%d %H:%M:%S") + "'")
    tempRow = cursor.fetchone()  
    while tempRow:  
        row = tempRow
        tempRow = cursor.fetchone() 

    disk = json.loads(row[4])
    result = CustomSensorResult("this sensor is kevin's test")
    
    conn.close()

    for diskInfo in disk:
        result.add_channel(channel_name=diskInfo['name'] + " 使用率", unit="Percent", value=diskInfo['usage_rate'], is_float=True, is_limit_mode=True, limit_max_error=80, limit_error_msg="剩餘空間不足")
        result.add_channel(channel_name=diskInfo['name'] + " 剩餘", unit="GByte", value=diskInfo['free'], is_float=True)
        result.add_channel(channel_name=diskInfo['name'] + " 共", unit="GByte", value=diskInfo['total'], is_float=True)
    
    print(result.get_json_result())
