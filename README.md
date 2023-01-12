# pysensorpush-gatt

Python library which uses gatttool to read temperature data from a Sensorpush HT.w temperature sensor.

1. Find the mac address of your sensor:<br>
```
pi@raspberrypi:~ $ sudo hcitool lescan
LE Scan ...
A4:34:F1:7F:CD:D8 SensorPush HT.w CDD8
```

2. Example usage:
```
$ python3
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> import sensorpush
>>> sensorpush.connect("A4:34:F1:7F:CD:D8")
Connecting to A4:34:F1:7F:CD:D8...
>>> volts, rawTemp = sensorpush.read_batt_info()
>>> print(volts, rawTemp)
3.156 16
>>> ts = sensorpush.read_timestamp()
>>> print (ts)
1915
>>> did = sensorpush.read_device_id()
>>> print(did)
16816765
>>> rev = sensorpush.read_revision_code()
>>> print(rev)
001_000.001_030.003_000.002
>>> si = sensorpush.read_sample_interval()
>>> print(si)
60
```

![pysensorpush_pic](https://user-images.githubusercontent.com/5443337/143657088-2a6d5793-24d3-4408-9d07-30b3f3f04577.jpg)
