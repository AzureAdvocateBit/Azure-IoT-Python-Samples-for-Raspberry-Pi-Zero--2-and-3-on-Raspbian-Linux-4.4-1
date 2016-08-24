# Rasperry Pi Rasbian Linux and Azure IoT Hub Secure Sensor Data Streaming


Rasperry Pi Rasbian and Azure IoT hub Sensor Streaming Samples


## Hardware Required

As at August 2016

1. Raspberry Pi Zero, Raspberry Pi 2 or 3
1. Tested on Raspbian Kernel 4.4 fully patched

## HATS (Hardware Attached on Top)

Optional but useful, these samples are built using the following HATS. 

1. [Enviro pHAT](https://shop.pimoroni.com/products/enviro-phat) for temperature, barometric, and light sensing
1. [Raspberry Pi Sense HAT](https://www.raspberrypi.org/products/sense-hat/)

## Process to build the IOT SDK for Rasbian Linux

As at August 2016 the samples include the compiled iothub_client.so library for ARM V6 (Pi Zero) and V7 (Pi 2 and 3).

To compile your own iothub_client.so library follow these instructions. 

1. Increase Raspberry Pi Swap File size - see notes below
2. [Overview of preparing your Python Development Environment](https://github.com/Azure/azure-iot-sdks/blob/master/doc/get_started/python-devbox-setup.md)
3. [Compile Azure IoT Device SDK for C](https://github.com/Azure/azure-iot-sdks/blob/master/c/doc/devbox_setup.md#linux)
4. [Compile Azure IoT Python Libraries](https://github.com/Azure/azure-iot-sdks/blob/master/doc/get_started/python-devbox-setup.md#linux)





## Recommended Software

1. To find your Raspberry Pi on your network by name install [Apple Print Bonjour Service](https://support.apple.com/kb/dl999?locale=en_AU) on Windows for mDNS UNIX Name Resolution. .
2. My favourite SSH and SFTP Windows Client is [Bitvise](https://www.bitvise.com/)
3. [Visual Studio Code](https://code.visualstudio.com/) for Windows, Mac and Linux

## Recommended Raspbian Packages

1. For Windows Remote Desktop Connection Support 

    sudo apt-get install xrdp

### Handy Tip for Raspberry Pi Zero

[Raspberry Pi Zero – Programming over USB](http://blog.gbaman.info/?p=791) ONLY works with Raspberry Pi Zero and provides a quick easy way to connect your PC to your Raspberry Pi Zero.



## Increase the Raspberry Pi Swap File Size

To compile Azure SDK on the Raspberry Pi you will almost certainly need to temporarily increase the size of the swap file.
See [How to change Raspberry Pi's Swapfile Size on Raspbian](https://www.bitpi.co/2015/02/11/how-to-change-raspberry-pis-swapfile-size-on-rasbian/)

**Be sure to change the swapfile size back to the default after the SDK has been compiled.**

## Follow these steps

#### Edit Swap File Configuration

    
    sudo nano /etc/dphys-swapfile

The default value in Raspbian is:

    CONF_SWAPSIZE=100

Change this to:

    CONF_SWAPSIZE=1024

Save changes

#### Restart Swap File Service


    sudo /etc/init.d/dphys-swapfile stop
    sudo /etc/init.d/dphys-swapfile start

#### Verify Swap File Size


    free -m

The output should look like:

    total     used     free   shared  buffers   cached
    Mem:           435       56      379        0        3       16
    -/+ buffers/cache:       35      399
    Swap:         1023        0     1023

#### Reset Swap File Size After compile

Be sure to change the swapfile size back to the default after the SDK has been compiled.






