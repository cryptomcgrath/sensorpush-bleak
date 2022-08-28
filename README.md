# pysensorpush

Simple python library which gatttool to read temperature data from a Sensorpush HT.w temperature sensor.


1. Install bluez-5.62 (download, configure, make, install install onto your PI device)<br>
see https://www.jaredwolff.com/get-started-with-bluetooth-low-energy/<br>

2. Use hcitool to find your Sensorpush mac address:<br>
```
pi@raspberrypi:~ $ sudo hcitool lescan<br>
LE Scan ...<br>
A4:34:F1:7F:CD:D8 SensorPush HT.w CDD8<br>
```

3. Edit sensor.py, change this line<br>
```
DEFAULT_SENSOR_ADDR="A4:34:F1:7F:CD:D8"<br>
```
to use your own device's mac address that you found using hcitool above<br>

4. Execute run_demo.sh which will execute the python script sensor_demo.py and will demonstrate some of the library function in sensor.py

![pysensorpush_pic](https://user-images.githubusercontent.com/5443337/143657088-2a6d5793-24d3-4408-9d07-30b3f3f04577.jpg)
