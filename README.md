# pysensorpush

Simple python library which gatttool to read temperature data from a Sensorpush HT.w temperature sensor.

1. Use hcitool to find your Sensorpush mac address:<br>
```
pi@raspberrypi:~ $ sudo hcitool lescan
LE Scan ...
A4:34:F1:7F:CD:D8 SensorPush HT.w CDD8
```

2. Edit sensor.py, change this line<br>
```
DEFAULT_SENSOR_ADDR="A4:34:F1:7F:CD:D8"
```
to use your own device's mac address that you found using hcitool above<br>

3. Example usage:
```
$ python3
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> import sensorpush
>>> sensorpush.connect()
Connecting to A4:34:F1:7F:CD:D8...
>>> volts, rawTemp = sensorpush.read_batt_info()
>>> print(volts, rawTemp)
3.156 16
>>> 

```

![pysensorpush_pic](https://user-images.githubusercontent.com/5443337/143657088-2a6d5793-24d3-4408-9d07-30b3f3f04577.jpg)
