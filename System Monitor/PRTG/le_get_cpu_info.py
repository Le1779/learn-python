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

    cpu = json.loads(row[2])
    result = CustomSensorResult("this sensor is kevin's test")
    
    conn.close()

    for i in range(len(cpu['usage_rate'])):
            print(cpu['usage_rate'][i])
            result.add_channel(channel_name="Processor" + str(i), unit="Percent", value=cpu['usage_rate'][i], is_float=True)
    print(result.get_json_result())
