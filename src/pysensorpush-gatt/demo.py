#!/usr/bin/env python3

import sensorpush as sp
from bleak import BleakClient
import asyncio
import utils as ut

async def main():
    address = "18:04:ED:FB:08:24"
    async with BleakClient(address) as client:
        volts, temp = await sp.read_batt_info(client) 
        print("volts={}, temp={}".format(volts, temp))

        ts = await sp.read_timestamp(client)
        print("timestamp = {}".format(ts))

        device_id = await sp.read_device_id(client)
        print("device id = {}".format(device_id))

        revision = await sp.read_revision_code(client)
        print("revision = {}".format(revision))

        sample_interval = await sp.read_sample_interval(client)
        print("sample interval = {}".format(sample_interval))

        temp = await sp.read_temperature(client)
        temp_f = ut.celsiusToFahrenheit(temp)
        print("temperature = {} celsius, {} fahrenheit".format(temp, temp_f))

        hum = await sp.read_humidity(client)
        print("humidity = {}".format(hum))

asyncio.run(main())        
