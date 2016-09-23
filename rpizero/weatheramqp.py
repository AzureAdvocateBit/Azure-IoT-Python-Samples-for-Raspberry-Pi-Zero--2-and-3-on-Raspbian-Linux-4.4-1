#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# Weather from https://github.com/csparpa/pyowm
# pip3 install pyowm

# Enviro pHAT install with 
# curl -sS https://get.pimoroni.com/envirophat | bash 

import iothub_client
from iothub_client import *
import time
import sys

sys.path[0:0] = ['../common'] ## path to shared owm.py (open weather map) and iothub.py (azure iot hub python) files

import owm 
import iothub

from envirophat import light, weather, leds



sensorLocation = "Melbourne"
owmLocation = 'Melbourne,AU'
iothubConnectionString = 'HostName=IoTCampAU.azure-devices.net;DeviceId=pizero;SharedAccessKey=uJ21qp9LUvlOSipkXusvlRoYwmUDE+4gXyIYS00feZg='
openWeather = owm.Weather('c204bb28a2f9dc23925f27b9e21296dd', owmLocation)
iot = iothub.IotHub(iothubConnectionString)
msg_txt = "{\"Geo\":%s,\"Light\":%d,\"HPa\":%d,\"Celsius\": %.2f,\"Id\":%d}"


def callback(message, properties):
    print(message)
    print("Properties: %s" % properties)


def iothub_client_sample_run():
    id = 0  

    iot.initialise(callback)

    while True:
        try:
            leds.on()

            openWeather.getWeather()
            id += 1

            ## normalise light to something of 100%
            lightLevel = light.light();
            if lightLevel > 1024:
                lightLevel = 1024            
            lightLevel = lightLevel * 100 / 1024

            msg_txt_formatted = msg_txt % (sensorLocation, lightLevel, round(weather.pressure()/100,2),  round(weather.temperature(),2), id)
            
            iot.publish(msg_txt_formatted, id)

            leds.off()
            time.sleep(4)

        except IoTHubError as e:
            print("Unexpected error %s from IoTHub" % e)
            print_last_message_time(iot.iotHubClient)
            time.sleep(4)
        
        except KeyboardInterrupt:
            print("IoTHubClient sample stopped")
            return

def configInfo():
    iot.version()
    openWeather.config()
    print('Sensor Location: ' + sensorLocation)
    print()
    print("Starting the Open Weather Map Azure IoT Hub Python sample...")
    print()


if __name__ == '__main__':
    configInfo()
    iothub_client_sample_run()
