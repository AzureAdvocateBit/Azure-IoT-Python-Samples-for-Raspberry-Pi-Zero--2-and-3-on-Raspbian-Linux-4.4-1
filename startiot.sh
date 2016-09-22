#!/bin/bash
echo "starting IoT Hub Client"

sleep 10

sudo killall python3

cd /home/pi/iothub/rpi2

python3 weather.py&

