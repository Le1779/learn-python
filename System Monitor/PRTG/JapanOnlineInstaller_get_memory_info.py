#!..\..\redist\Python34
# -*- coding: utf-8 -*-

from paepy.ChannelDefinition import CustomSensorResult
import sys
import json
import pymssql
import datetime
deviceID = 19
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

    memory = json.loads(row[3])
    result = CustomSensorResult("this sensor is kevin's test")
    
    conn.close()

    result.add_channel(channel_name="使用率", unit="Percent", value=memory['usage_rate'], is_float=True)
    result.add_channel(channel_name="free", unit="GByte", value=memory['free'], is_float=True)
    result.add_channel(channel_name="total", unit="GByte", value=memory['total'], is_float=True)
    
    print(result.get_json_result())
