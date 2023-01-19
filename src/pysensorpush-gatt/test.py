import asyncio
from bleak import BleakScanner, BleakClient
import utils as ut
import sensorpush as sp

UUID_REVISION="ef090002-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 15): Unknown
UUID_DEVICE_ID="ef090001-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 13): Unknown
UUID_BATT_INFO="ef090007-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 23): Unknown
UUID_TIMESTAMP="ef090008-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 25): Unknown
UUID_SAMPLE_INTERVAL="ef090004-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 19): Unknown
UUID_TEMP_GET="ef090080-11d6-42ba-93b8-9dd7ec090aa9" #(Handle: 38): Unknown
UUID_HUM_GET="ef090081-11d6-42ba-93b8-9dd7ec090aa9"

# read returns single byte of 5
UUID_17="ef090003-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 17): Unknown

UUID_21="ef090005-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 21): Unknown
UUID_27="ef090009-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 27): Unknown
UUID_29="ef09000a-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 29): Unknown
UUID_32="ef09000b-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 32): Unknown
UUID_34="ef09000c-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 34): Unknown
UUID_36="ef09000d-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 36): Unknown
UUID_40="ef090081-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 40): Unknown

#f000ffc5-0451-4000-b000-000000000000 (Handle: 49): Unknown
#f000ffc2-0451-4000-b000-000000000000 (Handle: 46): Unknown
#f000ffc1-0451-4000-b000-000000000000 (Handle: 43): Unknown

async def main():
    #devices = await BleakScanner.discover()
    #for d in devices:
    #    print("address = {} name = {} details = {}".format(d.address, d.name, d.details))
    
    address = "18:04:ED:FB:08:24"
    async with BleakClient(address) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)
            for c in service.characteristics:
                print("    {}".format(c))

        # returns r29=bytearray(b'\xe1\xe6\xc6cN\x81\xf4@\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        r29 = await client.read_gatt_char(UUID_29)
        print("r29={}".format(r29))
        hex29 = ut.bytesToHexStr(r29)
        print("hex29={}".format(hex29))
        samples = sp.decode_values(r29)
        for i in range(0, len(samples)):
            sample = samples[i]
            print("sample {} time={} temp_c={} hum={}".format(i, sample.ts_first, sample.temp_c, sample.hum))

        r27 = await client.read_gatt_char(UUID_27)
        print("r27={}".format(r27))
        samples = sp.decode_values(r27)
        for i in range(0, len(samples)):
            sample = samples[i]
            print("sample {} time={} temp_c={} hum={}".format(i, sample.ts_first, sample.temp_c, sample.hum))

asyncio.run(main())
