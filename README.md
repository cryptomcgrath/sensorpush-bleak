# pysensorpush-bleak

Python library which uses bleak to read temperature data from a Sensorpush HT.w temperature sensor.

1. Find the mac address of your sensor:<br>
```
pi@raspberrypi:~ $ sudo hcitool lescan
LE Scan ...
A4:34:F1:7F:CD:D8 SensorPush HT.w CDD8
```

2. Example usage:
```
$ pip install sensorpush-bleak
...
Successfully installed sensorpush-bleak-1.0.7
$ python
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from sensorpush import sensorpush as sp
>>> import asyncio
>>> from bleak import BleakClient
>>> async def main():
...     client = BleakClient("A4:34:F1:7F:CD:D8")
...     await client.connect()
...     temp_c = await sp.read_temperature(client)
...     print("temperature = {}".format(temp_c))
...     client.disconnect()
...
>>> asyncio.run(main())
temperature = 13.92
>>>
```
![pysensorpush_pic](https://user-images.githubusercontent.com/5443337/143657088-2a6d5793-24d3-4408-9d07-30b3f3f04577.jpg)
