# pysensorpush-bleak

Python library which uses bleak to read temperature data from a Sensorpush HT.w temperature sensor.

1. Find the address of your sensor

#### Using hcitool

```
pi@raspberrypi:~ $ sudo hcitool lescan
LE Scan ...
A4:34:F1:7F:CD:D8 SensorPush HT.w CDD8
```

#### Using the Builtin Scanner

Note that:

* MacOS returns a virtual address in the form of a UUID and not the actual MAC
  address.
* The error message `BLE is not authorized` indicates the process does not have
  permission to access bluetooth on MacOS

```python
from sensorpush import sensorpush as sp

async def main():
    devices = await sp.scan()
    for d in devices:
        print(f'{d.address} {d.name}')

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    pass
```

If you have more than 1 device then tell the scanner to wait until multiple devices are found:

`sp.scan(device_count=2)`

To change the timeout in seconds (default=30):

`sp.scan(timeout=10)`

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
