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

3. There is a demo in ```__main__.py``` which exercices some of the api in sensorpush.py

4. To read the current temperature:
```
import sensorpush
temp = sensorpush.read_temperature()
print("The temperature is {}".format(temp))
```

![pysensorpush_pic](https://user-images.githubusercontent.com/5443337/143657088-2a6d5793-24d3-4408-9d07-30b3f3f04577.jpg)
