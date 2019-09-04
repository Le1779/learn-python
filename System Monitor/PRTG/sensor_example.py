# -*- coding: utf-8 -*-

import sys
import json
# get CustomSensorResult from paepy package
from paepy.ChannelDefinition import CustomSensorResult

if __name__ == "__main__":
    # interpret first command line parameter as json object
    data = json.loads(sys.argv[1])

    # create sensor result
    result = CustomSensorResult("This sensor is added to " + data['host'])

    # add primary channel
    result.add_channel(channel_name="Percentage", unit="Percent", value=87, is_float=False, primary_channel=True,
                       is_limit_mode=True, limit_min_error=10, limit_max_error=90,
                       limit_error_msg="Percentage too high")
    # add additional channel
    result.add_channel(channel_name="Response Time", unit="TimeResponse", value="4711")
    # print sensor result to std
    print(result.get_json_result())
