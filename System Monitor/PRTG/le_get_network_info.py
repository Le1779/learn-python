#!..\..\redist\Python34
# -*- coding: utf-8 -*-

from paepy.ChannelDefinition import CustomSensorResult
import sys
import json
import pymssql
import datetime
deviceID = 8
if __name__ == "__main__":
    conn = pymssql.connect(server='10.0.0.55', user='DFO_Trial', password='DynaCW999', database='SystemMonitor')
    cursor = conn.cursor()
    endDate = datetime.datetime.now()
    startDate = endDate - datetime.timedelta(0, 120)
    cursor.execute("SELECT * FROM DeviceInfo WHERE DeviceID = '" + str(deviceID) + "' AND UpdateTime BETWEEN '" + startDate.strftime("%Y/%m/%d %H:%M:%S") + "' AND '" + endDate.strftime("%Y/%m/%d %H:%M:%S") + "'")
    row = cursor.fetchone()  

    network = json.loads(row[5])
    result = CustomSensorResult("this sensor is kevin's test")
    
    conn.close()

    result.add_channel(channel_name="使用率", unit="kbit", value=network['usage']/1024.*8, is_float=True)
    result.add_channel(channel_name="接收", unit="kbit", value=network['receive']/1024.*8, is_float=True)
    result.add_channel(channel_name="傳送", unit="kbit", value=network['send']/1024.*8, is_float=True)
    
    print(result.get_json_result())
