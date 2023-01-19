import utils as ut
import sensorpush_parser
import asyncio

STOP_TOKEN_B = b'\xff\xff\xff\xff'

UUID_REVISION="ef090002-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 15): Unknown
UUID_DEVICE_ID="ef090001-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 13): Unknown
UUID_BATT_INFO="ef090007-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 23): Unknown
UUID_TIMESTAMP="ef090008-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 25): Unknown
UUID_SAMPLE_INTERVAL="ef090004-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 19): Unknown
UUID_TEMPERATURE="ef090080-11d6-42ba-93b8-9dd7ec090aa9" #(Handle: 38): Unknown
UUID_HUMIDITY="ef090081-11d6-42ba-93b8-9dd7ec090aa9"

#### UNKNOWN CHARACTERISTICS ####
# read returns single byte of 5
UUID_17="ef090003-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 17): Unknown
# read returns two bytes 0808 (int 2056)
UUID_21="ef090005-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 21): Unknown
# read returns bulk values bytes
UUID_27="ef090009-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 27): Unknown
# read returns bulk values bytes
UUID_29="ef09000a-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 29): Unknown

UUID_32="ef09000b-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 32): Unknown
UUID_34="ef09000c-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 34): Unknown
UUID_36="ef09000d-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 36): Unknown
UUID_40="ef090081-11d6-42ba-93b8-9dd7ec090aa9" # (Handle: 40): Unknown
UUID_49="f000ffc5-0451-4000-b000-000000000000" # (Handle: 49): Unknown
UUID_46="f000ffc2-0451-4000-b000-000000000000" # (Handle: 46): Unknown
UUID_43="f000ffc1-0451-4000-b000-000000000000" # (Handle: 43): Unknown

class Sample:
    ts_first = None
    temp_c = None
    hum = None

    def __init__(self, ts_first, temp_c, hum):
       self.ts_first = ts_first
       self.temp_c = temp_c
       self_hum = hum
 
async def read_batt_info(client):
  """
  Reads the battery info and returns volts, rawTemp

  Args:
    client : The bleak client

  Returns:
    volts (float), rawTemp (float)
  """
  bs = await client.read_gatt_char(UUID_BATT_INFO)
  b_volts = bs[0:2]
  b_temp = bs[2:4]
  volts = ut.bytesToInt(b_volts) / 1000
  rawTemp = ut.bytesToInt(b_temp)
  return volts, rawTemp

async def write_timestamp(client, ts_secs):
  """
  Writes the timestamp to the device
  (sets the current time)

  Args:
    client: The bleak client
    ts_secs (int): The timestamp in seconds since epoch
  """ 
  ts_b = ut.intToBytes(ts_secs)
  await client.write_gatt_char(UUID_TIMESTAMP, ts_b)

async def read_timestamp(client):
  """
  Reads the timestamp of the device

  Args:
    client : The bleak client

  Returns:
    (int): timestamp in seconds since epoch
  """
  ts_b = await client.read_gatt_char(UUID_TIMESTAMP)
  return ut.bytesToInt(ts_b)

async def read_device_id(client):
  """
  Reads the device id of the device

  Args:
    client : The bleak client

  Returns:
    The device id as an int
  """
  device_b = await client.read_gatt_char(UUID_DEVICE_ID)
  return ut.bytesToInt(device_b)

async def read_revision_code(client):
  """
  Returns the device revision code string
  
  Args:
    client : The bleak client

  Returns:
    The device revision code string
  """
  rev_b = await client.read_gatt_char(UUID_REVISION)
  i1 = ut.bytesToInt(rev_b[0:1])
  i2 = ut.bytesToInt(rev_b[1:2])
  i3 = ut.bytesToInt(rev_b[2:3])
  i4 = ut.bytesToInt(rev_b[3:4])
  i5 = ut.bytesToInt(rev_b[4:5])
  i6 = ut.bytesToInt(rev_b[5:6])
  i7 = ut.bytesToInt(rev_b[6:7])
  rev_str = "{:0>3}_{:0>3}.{:0>3}_{:0>3}.{:0>3}_{:0>3}.{:0>3}".format(i1, i2, i3, i4, i5, i6, i7)
  return rev_str

async def read_sample_interval(client):
  """
  Reads the sample interval in seconds

  Args:
    client : The bleak client

  Returns:
    Sample interval in seconds (int)
  """
  sample_interval_b = await client.read_gatt_char(UUID_SAMPLE_INTERVAL)
  return ut.bytesToInt(sample_interval_b)

async def read_temperature(client):
    dummy_b = b'\x01\x00\x01\x00'
    await client.write_gatt_char(UUID_TEMPERATURE, dummy_b)
    await asyncio.sleep(.11)
    temp_b = await client.read_gatt_char(UUID_TEMPERATURE)
    temp = ut.bytesToInt(temp_b) / 100
    return temp

async def read_humidity(client):
    dummy_b = b'\x01\x00\x01\x00'
    await client.write_gatt_char(UUID_HUMIDITY, dummy_b)
    await asyncio.sleep(.11)
    hum_b = await client.read_gatt_char(UUID_HUMIDITY)
    hum = ut.bytesToInt(hum_b) / 100
    return hum

def decode_values(values):
    """
    Decodes sensorpush notification values bytes
    
    Args:
        values (bytearray): The values bytearray returned from the bulk read 

    Returns:
        Sample[] or None
    """
    if len(values) < 8:
        return None

    # This is the portion of the values containing the timestamp
    sample_time_b = values[0:4]
    if sample_time_b == STOP_TOKEN_B:
        return None

    sample_time_int = ut.bytesToInt(sample_time_b)

    ### This is the portion of the values containing the temp, humidity readings
    sample_readings_b = values[4:]

    ### chop the readings string into an array, each element is 4 bytes
    samples = []
    n_bytes = int(len(sample_readings_b) / 4) * 4
    for i in range(0,n_bytes, 4):
        samples.append(sample_readings_b[i:i+4])
        
    result = [] 
    for j in range(len(samples)-1, -1, -1):
        sample = samples[j]
        print("sample {} = {}".format(j, sample))
        if sample != STOP_TOKEN_B:
            ## add dummy byte to beginning
            sample_bytes = bytearray([65])
            sample_bytes += samples[j]
            vals = sensorpush_parser.decode_values(sample_bytes, 65)
            temp_c = vals["temperature"]
            hum = vals["humidity"]
            result.append(Sample(sample_time_int, temp_c, hum))

    return result
