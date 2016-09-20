import time
import owm
import iothub

w = owm.Weather('c204bb28a2f9dc23925f27b9e21296dd', 'Sydney,au')
iot = iothub.IotHub('HostName=IoTCampAU.azure-devices.net;DeviceId=UbuntuSB4;SharedAccessKey=ATLRGx7qgUOwCIT1o3l2XJTidEyQmD7fSpKGZfrGViw=')


while True:
    w.getWeather()
    print('Temperature: ' + str(w.temperature))
    print('Pressure: ' + str(w.pressure))
    print('Humidity: ' + str(w.humidity))
    time.sleep(4)
