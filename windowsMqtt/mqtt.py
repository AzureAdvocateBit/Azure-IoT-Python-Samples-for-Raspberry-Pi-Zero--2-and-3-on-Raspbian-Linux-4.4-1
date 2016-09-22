# HostName=IoTCampAU.azure-devices.net;DeviceId=mqtt;SharedAccessSignature=SharedAccessSignature sr=IoTCampAU.azure-devices.net%2fdevices%2fmqtt&sig=tQz78YxYsyRCDCTOPGMIrYFhYByPc26FCfCfB%2b6HgBI%3d&se=1491831743
# https://azure.microsoft.com/en-us/documentation/articles/iot-hub-mqtt-support/
# http://stackoverflow.com/questions/35452072/python-mqtt-connection-to-azure-iot-hub/35473777
# https://github.com/bechynsky/AzureIoTDeviceClientPY


import paho.mqtt.client as mqtt


hubAddress = 'IoTCampAU.azure-devices.net'
hubName = 'mqtt'
hubPass = 'SharedAccessSignature sr=IoTCampAU.azure-devices.net%2fdevices%2fmqtt&sig=o7YAZr8jJYITgFKG1fIVi2pIfmof%2bTHSHCmYCky%2fzJE%3d&se=1478873518'
hubUser = hubAddress + '/' + hubName
hubTopicPublish = 'devices/' + hubName + '/messages/events/'
hubTopicSubscribe = 'devices/' + hubName + '/messages/devicebound/#'



def on_connect(client, userdata, flags, rc):
    print( "Connected with result code: %s" % rc)
    client.subscribe(hubTopicSubscribe)
    client.publish(hubTopicPublish, "test")


def on_disconnect(client, userdata, rc):
    print( "Disconnected with result code: %s" % rc)


def on_message(client, userdata, msg):
    print( " - ".join((msg.topic, str(msg.payload))))
    # Do this only if you want to send a reply message every time you receive one
    client.publish("devices/<YOUR DEVICE ID>/messages/events", "REPLY", qos=1)


def on_publish(client, userdata, mid):
    print("Sent message")


client = mqtt.Client(hubName, mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_message = on_message
#client.on_publish = on_publish

client.username_pw_set(hubUser, hubPass)
client.tls_insecure_set(True) # You can also set the proper certificate using client.tls_set()

client.connect_async(hubAddress, 8883)


client.loop_forever()

