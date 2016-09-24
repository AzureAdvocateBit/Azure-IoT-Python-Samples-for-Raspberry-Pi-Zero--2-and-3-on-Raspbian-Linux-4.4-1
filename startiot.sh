#!/bin/bash
echo "starting IoT Hub Client"

sleep 10

sudo killall python3

cd /home/pi/iothub/weather_mqtt

python3 weather_mqtt.py "sensor_envirophat" "pizero" "uJ21qp9LUvlOSipkXusvlRoYwmUDE+4gXyIYS00feZg="&

