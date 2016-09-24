# https://azure.microsoft.com/en-us/documentation/articles/iot-hub-mqtt-support/
# http://stackoverflow.com/questions/35452072/python-mqtt-connection-to-azure-iot-hub/35473777
# https://azure.microsoft.com/en-us/documentation/samples/iot-hub-python-get-started/

# Mqtt Support https://www.eclipse.org/paho/clients/python/
# pip3 install paho-mqtt

# Weather data Open Weather Map using https://github.com/csparpa/pyowm
# pip3 install pyowm

import sys
import paho.mqtt.client as mqtt
import time
import base64
import hmac
import urllib.parse
sys.path[0:0] = ['../common'] ## path to shared owm.py (open weather map) and iothub.py (azure iot hub python) files
import owm 


hubAddress = 'IoTCampAU.azure-devices.net'
hubName = 'mqtt'
SharedAccessKey= 'VZbmLwYjjdg04Gb5SvbNMTq44GdDEO5k5px6OUIu7l8='

endpoint = hubAddress + '/devices/' + hubName
hubUser = hubAddress + '/' + hubName
hubTopicPublish = 'devices/' + hubName + '/messages/events/'
hubTopicSubscribe = 'devices/' + hubName + '/messages/devicebound/#'

sensorLocation = "Melbourne"
owmLocation = 'Melbourne, AU'
iothubConnectionString = 'HostName=IoTCampAU.azure-devices.net;DeviceId=WindowsPython35;SharedAccessKey=GqtVoi57XA3oViEWvHJSX9QNBHho9H747AtgjUdxh1Q='
openWeather = owm.Weather('c204bb28a2f9dc23925f27b9e21296dd', owmLocation)
msg_txt = "{\"Geo\":%s,\"Humidity\":%d,\"HPa\":%d,\"Celsius\": %.2f,\"Light\":%d,\"Id\":%d}"


# sas generator from https://github.com/bechynsky/AzureIoTDeviceClientPY/blob/master/DeviceClient.py
def generate_sas_token(uri, key, expiry=4320000): # 50 day expiry
    ttl = int(time.time()) + expiry
    urlToSign = urllib.parse.quote(uri, safe='') 
    sign_key = "%s\n%d" % (urlToSign, int(ttl))
    h = hmac.new(base64.b64decode(key), msg = "{0}\n{1}".format(urlToSign, ttl).encode('utf-8'),digestmod = 'sha256')
    signature = urllib.parse.quote(base64.b64encode(h.digest()), safe = '')
    return "SharedAccessSignature sr={0}&sig={1}&se={2}".format(urlToSign, urllib.parse.quote(base64.b64encode(h.digest()), safe = ''), ttl)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %s" % rc)
    client.subscribe(hubTopicSubscribe)

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s" % rc)

def on_message(client, userdata, msg):
    print(" - ".join((msg.topic, str(msg.payload))))
    # Do this only if you want to send a reply message every time you receive one
    #client.publish("devices/mqtt/messages/events", "REPLY", qos=1)

def on_publish(client, userdata, mid):
    print("Message {0} sent from {1}".format(str(mid), hubName))

def publish():
    id = 0  

    while True:
        try:
            openWeather.getWeather()
            lightLevel = 0
            id += 1            

            msg_txt_formatted = msg_txt % (sensorLocation, openWeather.humidity, openWeather.pressure, openWeather.temperature, lightLevel, id)
            
            client.publish(hubTopicPublish, msg_txt_formatted)
            
            time.sleep(4)
        
        except KeyboardInterrupt:
            print("IoTHubClient sample stopped")
            return

        except:
            print("Unexpected error")
            time.sleep(4)


client = mqtt.Client(hubName, mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish

client.username_pw_set(hubUser, generate_sas_token(endpoint, SharedAccessKey))

#client.tls_set("/etc/ssl/certs/ca-certificates.crt") # use builtin cert on Raspbian
client.tls_set("baltimorebase64.cer") # Baltimore Cybertrust Root exported using certlm.msc in base64 format
client.connect(hubAddress, 8883)

client.loop_start()

publish()