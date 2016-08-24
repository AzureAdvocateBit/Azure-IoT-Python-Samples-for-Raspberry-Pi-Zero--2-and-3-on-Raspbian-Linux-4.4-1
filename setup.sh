#!/bin/bash

echo setting up IoT Client Startup Services

sudo chmod +x python3/iothubclient.py
sudo chmod +x startiot.sh


sudo cp iot.service /etc/systemd/system

sudo systemctl enable iot.service
sudo systemctl start iot.service
sudo systemctl status iot.service
