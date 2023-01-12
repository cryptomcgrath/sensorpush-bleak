import pexpect
import utils as ut
import sensorpush_parser
import sys
import asyncio

# change this to your sensor address
# use hcitool to find it:
#   sudo hcitool lescan
#
DEFAULT_SENSOR_ADDR="A4:34:F1:7F:CD:D8"

# bluetooth characteristic handles
HND_BATT_INFO = "0x0018"
HND_TIMESTAMP = "0x1a"
HND_SAMPLE_INTERVAL = "0x0014"
HND_REVISION_CODE = "0x0010"
HND_DEVICE_ID = "0x000e"
HND_BULK_READ = "0x001c"
HND_ADV_INTERVAL = "0x0016"
HND_MODE = "0x001f"

RESPONSE_WRITE_SUCCESS = "Characteristic value was written successfully\r\n"
RESPONSE_READ_SUCCESS = "Characteristic value/descriptor: "
STOP_TOKEN = "ffffffff"

TIMEOUT=10

child=pexpect.spawn("gatttool -I")

#
# connects to the device specified by addr
#
# addr : str 
#     The mac address of the device to connect to as a string in the format A1:B2:C3:D4:E5:F6
#
def connect(addr = DEFAULT_SENSOR_ADDR):
  print("Connecting to "+addr+"..."),
  try:
      child.sendline("connect {0}".format(addr))
      child.expect("Connection successful", timeout=TIMEOUT)
  except:
      print("connect error", sys.exc_info()[0])
  return

# read bluetooth characteristic handle
# 
# hnd : str
#     The handle to read (see the list of bluetooth characteristic handles above
#
def read_hnd(hnd):
  try:
      child.sendline("char-read-hnd "+hnd)
      child.expect(RESPONSE_READ_SUCCESS, timeout=TIMEOUT)
      child.expect("\r\n", timeout=TIMEOUT)
      hex_str = child.before.decode().replace(" ","")
      return hex_str
  except:
      print("connect error", sys.exc_info()[0])
      return ""

# write bluetooh characteristic handle
#
# hnd : str
#    The handle to write to (see the list of bluetooth characteristic handles above)
#
def write_req(hnd, val):
  try:
      child.sendline("char-write-req "+hnd+" "+val)
      child.expect(RESPONSE_WRITE_SUCCESS, timeout=TIMEOUT)
      return True
  except:
      return False

# reads the battery info and returns volts, rawTemp
def read_batt_info():
  hexStr = read_hnd(HND_BATT_INFO)
  voltHex = hexStr[0:4]
  tempHex = hexStr[4:8]
  volts = ut.hexStrToInt(voltHex) / 1000
  rawTemp = ut.hexStrToInt(tempHex)
  return volts, rawTemp

def write_timestamp(hex_str):
  write_req(HND_TIMESTAMP, hex_str)
  return ut.hexStrToInt(hex_str)

def read_timestamp():
  hex_str = read_hnd(HND_TIMESTAMP)
  if hex_str == "":
      return 0
  return ut.hexStrToInt(hex_str)

def read_device_id():
  hex_str = read_hnd(HND_DEVICE_ID)
  return ut.hexStrToInt(hex_str)

def read_revision_code():
  hex_str = read_hnd(HND_REVISION_CODE)
  i1 = ut.hexStrToInt(hex_str[0:2])
  i2 = ut.hexStrToInt(hex_str[2:4])
  i3 = ut.hexStrToInt(hex_str[4:6])
  i4 = ut.hexStrToInt(hex_str[6:8])
  i5 = ut.hexStrToInt(hex_str[8:10])
  i6 = ut.hexStrToInt(hex_str[10:12])
  i7 = ut.hexStrToInt(hex_str[12:14])
  rev_str = "{:0>3}_{:0>3}.{:0>3}_{:0>3}.{:0>3}_{:0>3}.{:0>3}".format(i1, i2, i3, i4, i5, i6, i7)
  return rev_str

#
# returns the sample interval (int) in seconds
# 
def read_sample_interval():
  hex_str = read_hnd(HND_SAMPLE_INTERVAL)
  return ut.hexStrToInt(hex_str)


#
# reads the bulk values from the given timestamp_hex_str
# executes the callback_fun for each line of bulk values read
#
# callback_fun(sample_time_int, samples_hexstr_array, raw_bytes)
#      sample_time_int : int
#           The start time for this line of data.  The first sample
#      in samples_hexstr_array is this at this time and each sample after is taken
#      using the sample interval that is set
#
#      samples_hexstr_arary : str[]
#          array of hex strings, each hex string is 8 in length  
#
#      raw_bytes : byte[]
#          Byte array containing the raw data returned
#
def read_bulk_values(timestamp_hex_str, callback_fun):
  write_req(HND_MODE, "0100")
  print("starting bulk read from "+timestamp_hex_str)
  write_req(HND_BULK_READ, timestamp_hex_str)

  found_stop = False
  while found_stop == False:
    try:
      child.expect("Notification handle = 0x001e value: ", timeout=10)
    except:
      print("no more data to read")
      break
    child.expect("\r\n")
    values = child.before.decode().replace(" ","")
    print("values = "+values)

    if len(values) < 16:
      print("No temp avail")
      found_stop = True
      break

    sample_time_hexstr = values[0:8]
    sample_time = ut.hexStrToInt(sample_time_hexstr)
    if sample_time_hexstr == STOP_TOKEN:
        sample_time = 0
        found_stop = True
    else:
        sample_time = ut.hexStrToInt(sample_time_hexstr)
    samples = ut.hexStrToSamples(values[8:])
    for sample in samples:
        if sample == STOP_TOKEN:
            found_stop = True

    callback_fun(sample_time, samples, ut.hexStrToBytes(values))

def read_first_value():
  ts = read_timestamp()
  if ts == 0:
      return None

  timestamp_hex_str = ut.intToHexStr(ts-60)

  success = write_req(HND_MODE, "0100")
  if success == False:
      return None
  print("starting bulk read from "+timestamp_hex_str)
  success = write_req(HND_BULK_READ, timestamp_hex_str)
  if success == False:
      return None

  found_stop = False
  while found_stop == False:
    try:
      child.expect("Notification handle = 0x001e value: ", timeout=10)
    except:
      print("no more data to read")
      break
    child.expect("\r\n")
    values = child.before.decode().replace(" ","")
    print("values = "+values)

    if len(values) < 16:
      print("No temp avail")
      found_stop = True
      break

    sample_time_hexstr = values[0:8]
    sample_time = ut.hexStrToInt(sample_time_hexstr)
    if sample_time_hexstr == STOP_TOKEN:
        sample_time = 0
        found_stop = True
    else:
        sample_time = ut.hexStrToInt(sample_time_hexstr)
    samples = ut.hexStrToSamples(values[8:])
    for sample in samples:
        if sample == STOP_TOKEN:
            found_stop = True

    rev = samples[::-1]
    for j in range(len(samples)-1, 0, -1):
        sample = samples[j]
        sample_hex = sample[0:8]
        if sample_hex != STOP_TOKEN:
            sample_bytes = ut.hexStrToBytes(sample_hex)
            ## add dummy byte to beginning
            sample_bytes = bytearray([65])+sample_bytes
            vals = sensorpush_parser.decode_values(sample_bytes, 65)
            temp_c = vals["temperature"]
            temp_f = ut.celsiusToFahrenheit(temp_c)
            print("read latest got temp {}".format(temp_f))
            return temp_f

    return None

    
def read_latest(callback_fun):
    ts = read_timestamp()
    
    def bulk_cb(sample_time_int, samples, raw):
        rev = samples[::-1]
        for j in range(len(samples)-1, 0, -1):
            sample = samples[j]
            sample_hex = sample[0:8]
            if sample_hex != STOP_TOKEN:
                sample_bytes = ut.hexStrToBytes(sample_hex)
                ## add dummy byte to beginning
                sample_bytes = bytearray([65])+sample_bytes
                vals = sensorpush_parser.decode_values(sample_bytes, 65)
                temp_c = vals["temperature"]
                temp_f = ut.celsiusToFahrenheit(temp_c)
                print("read latest got temp {}".format(temp_f))
                callback_fun(ts+60*j, temp_f)
                break

    read_start_time_hex = ut.intToHexStr(ts-60)
    read_bulk_values(read_start_time_hex, bulk_cb)


