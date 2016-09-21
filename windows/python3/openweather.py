#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# Weather from https://github.com/csparpa/pyowm
# pip and pip3 install pyowm

import iothub_client
from iothub_client import *
import time
import owm 
import iothub

sensorLocation = "Melbourne"
owmLocation = 'Melbourne,AU'
iothubConnectionString = 'HostName=IoTCampAU.azure-devices.net;DeviceId=WindowsPython35;SharedAccessKey=GqtVoi57XA3oViEWvHJSX9QNBHho9H747AtgjUdxh1Q='
openWeather = owm.Weather('c204bb28a2f9dc23925f27b9e21296dd', owmLocation)
iot = iothub.IotHub(iothubConnectionString)
msg_txt = "{\"Geo\":%s,\"Humidity\":%d,\"HPa\":%d,\"Celsius\": %.2f,\"Id\":%d}"


def callback(message, properties):
    print(message)
    print("Properties: %s" % properties)


def iothub_client_sample_run():
    id = 0  

    iot.initialise(callback)

    while True:
        try:
            openWeather.getWeather()
            id += 1

            msg_txt_formatted = msg_txt % (sensorLocation, openWeather.humidity, openWeather.pressure, openWeather.temperature, id)
            iot.publish(msg_txt_formatted, id)
            
            time.sleep(4)

        except IoTHubError as e:
            print("Unexpected error %s from IoTHub" % e)
            print_last_message_time(iot.iotHubClient)
            time.sleep(4)
        
        except KeyboardInterrupt:
            print("IoTHubClient sample stopped")
            return


if __name__ == '__main__':
    iot.version()
    print('Azure IoT Hub Connection String')
    print(iothubConnectionString)
    print()
    print('Open Weather Map Loaction: ' + owmLocation)
    print('Sensor Location: ' + sensorLocation)
    print("Starting the Open Weather Map Azure IoT Hub Python sample...")
    print()

    iothub_client_sample_run()
