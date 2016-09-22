import iothub_client
from iothub_client import *
import sys


class IotHub():

    connection_string = ''
    protocol = IoTHubTransportProvider.AMQP
    timeout = 241000
    minimum_polling_time = 9

    # messageTimeout - the maximum time in milliseconds until a message times out.
    # The timeout period starts at IoTHubClient.send_event_async. 
    # By default, messages do not expire.
    message_timeout = 10000

    receive_context = 0
    message_count = 1
    received_count = 0

    receive_callbacks = 0
    send_callbacks = 0


    def __init__(self, connectString):
        self.connection_string = connectString

    def publish(self, msg_txt_formatted, id):
        message = IoTHubMessage(bytearray(msg_txt_formatted, 'utf8'))
        self.iotHubClient.send_event_async(message, self.send_confirmation_callback, id)

    def version(self):
        print("\nPython %s" % sys.version)
        print("IoT Hub for Python SDK Version: %s" % iothub_client.__version__)
        print()
        print("Protocol %s" % self.protocol)
        print()
        print('Azure IoT Hub Connection String')
        print(self.connection_string)


    def send_confirmation_callback(self, message, result, user_context):
        print("Confirmation[%d] received for message with result = %s" % (user_context, result))

    def initialise(self, messageCallback):
        self.messageCallback = messageCallback
        # prepare iothub client
        iotHubClient = IoTHubClient(self.connection_string, self.protocol)
        # set the time until a message times out
        iotHubClient.set_option("messageTimeout", self.message_timeout)
        iotHubClient.set_message_callback(self.receive_message_callback, self.receive_context)
        self.iotHubClient = iotHubClient
        #return iotHubClient


    def receive_message_callback(self, message, counter):
        buffer = message.get_bytearray()
        size = len(buffer)
        #print("<<Received Message [%d]>>" % counter)
        
        map_properties = message.properties()
        key_value_pair = map_properties.get_internals()

        self.messageCallback(buffer[:size].decode('utf-8'), key_value_pair)

        return IoTHubMessageDispositionResult.ACCEPTED


    def print_last_message_time(self, iotHubClient):
        try:
            last_message = iotHubClient.get_last_message_receive_time()
            print("Last Message: %s" % time.asctime(time.localtime(last_message)))
            print("Actual time : %s" % time.asctime())
        except IoTHubClientError as e:
            if (e.args[0].result == IoTHubClientResult.INDEFINITE_TIME):
                print("No message received")
            else:
                print(e)
