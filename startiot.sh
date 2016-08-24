#!/bin/bash
echo "starting IoT Hub Client"

sleep 10

sudo killall python3

python3 /home/pi/iothub/rpi3/python3/pisensehat.py&

