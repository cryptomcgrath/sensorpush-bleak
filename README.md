# pysensorpush

Uses python and gatttool to read temperature data from a Sensorpush HT.w temperature sensor.

Requires:

Raspberry Pi
bluez-5.62 (download, configure, make, install install onto your PI device -- see https://www.jaredwolff.com/get-started-with-bluetooth-low-energy/)

Use hcitool to find your Sensorpush mac address:
pi@raspberrypi:~ $ sudo hcitool lescan
LE Scan ...
A4:34:F1:7F:CD:D8 SensorPush HT.w CDD8

Edit sensor.py, change the line
DEFAULT_SENSOR_ADDR="A4:34:F1:7F:CD:D8"
to use your own device's mac address that you found using hcitool above

The file sensor.py contains functions to read/write to your Sensorpush device
For a demonstration, execute run_demo.sh which will execute the python script sensor_demo.py

![pysensorpush_pic](https://user-images.githubusercontent.com/5443337/143657088-2a6d5793-24d3-4408-9d07-30b3f3f04577.jpg)
