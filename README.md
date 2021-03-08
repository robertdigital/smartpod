# smartpod
Software and control firmware for pod automation services

The current system uses the MQTT protocol on an Ethernet Backed TCP/IP Network. IoT devices are connected to ESP32 modules which communicate with a custom
server process running on a Raspberry Pi via Ethernet cable connected through an Ethernet switch.  The custom server component that runs on the Raspberry Pi handles incoming requests for streaming data and IoT device configuration and administration.

Software Specifications
------------------------
* [MQTT](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
* [CANopen](https://en.wikipedia.org/wiki/CANopen)

Drivers and 3rd Party Software
-------------------------------
* [CAN Driver for Pi](https://copperhilltech.com/what-is-socketcan/)
* [Mosquitto MQTT Broker](https://mosquitto.org/)

Hardware
-----------------------
* [Raspberry Pi 4 Model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* [ESP32 Modules](https://dronebotworkshop.com/esp32-intro/)
* [CAN Bus Interface](https://copperhilltech.com/pican-2-can-bus-interface-for-raspberry-pi/)
