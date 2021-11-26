import pexpect
import time
import binascii
import sys
import struct
import time
from datetime import datetime
import pytz
import numpy as np

DEVICE="A4:34:F1:7F:CD:D8"

print("Run gatttool...")
child=pexpect.spawn("gatttool -I")

print("Connecting to "),
print(DEVICE),

child.sendline("connect {0}".format(DEVICE))
child.expect("Connection successful", timeout=10)
print(" Connected!")

# function to transform hex string like "0a cd" into signed integer
def hexStrToInt(hexstr):
  hexstr = hexstr.replace(" ","")
  bs = binascii.unhexlify(hexstr)
  val = int.from_bytes(bs, byteorder='little')
  return val

def intToHexStr(i):
  return (i).to_bytes(4, byteorder='little').hex()

def hexStrToSamples(hexStr):
  strarr = [] 
  for i in range(0,len(hexStr), 8):
    strarr.append(hexStr[i:i+8])
  return strarr

def intToTimeStr(i):
  d = datetime.fromtimestamp(i, tz=pytz.utc)
  tz = pytz.timezone('America/Montreal')
  return d.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")

def hexStrToByteArray(hexStr):
  bs = binascii.unhexlify(hexStr)
  return bs

def byteArrayToHumidity(bs):
  #return relativeHumidityFromRawHumidity((bs[0] & 255) + ((bs[1] & 15) << 8))
  raw_hum = (bs[0] & 255) + ((bs[1] & 15) << 8)
  return raw_hum

def relativeHumidityFromRawHumidity(i):
  rh = (float(i) / pow(2, 12)) * 125.0 - 6.0
  if rh < 0.0:
    rh = 0.0
  if rh > 100.0:
    rh = 100.0
  return rh

def byteArrayToTemperature(bs):
#  return tempCelciusFromRawTemp(((bs[1] & 255) >> 4) + ((bs[2] & 255) << 4) + ((bs[3] & 3) << 12))
  raw_temp = ((bs[1] & 255) >> 4) + ((bs[2] & 255) << 4) + ((bs[3] & 3) << 12)
  return raw_temp
  #return tempCelciusFromRawTemp(raw_temp)

def tempCelciusFromRawTemp(t):
  return (float(t) / pow(2,14)) * 175.72 - 46.85

### get battery info
child.sendline("char-read-hnd 0x0018")
child.expect("Characteristic value/descriptor: ", timeout=10)
child.expect("\r\n", timeout=10)
batInfoHexStr = child.before.decode().replace(" ","")
batVoltageHex = batInfoHexStr[0:4]
batVoltage = hexStrToInt(batVoltageHex) / 1000
batTempHex = batInfoHexStr[4:8]
rawBatTemp = hexStrToInt(batTempHex)
batTemp = tempCelciusFromRawTemp(rawBatTemp)
print("battery info ("+batInfoHexStr+") voltage="+"{:>6.2f}".format(batVoltage) + " raw temp="+str(rawBatTemp) + " bat temp " + "{:>6.2f}".format(batTemp))

### current time   
curTime = int(time.time())
curTimeHexStr = intToHexStr(curTime)
print("Current time "),
print(curTime)
print("Current time hex "),
print(curTimeHexStr)

### set sensor time clock
##child.sendline("char-write-req 0x1a "+curTimeHexStr)
##child.expect("Characteristic value was written successfully\r\n", timeout=10)

### get last timestamp of data
child.sendline("char-read-hnd 0x1a")
child.expect("Characteristic value/descriptor: ", timeout=10)
child.expect("\r\n", timeout=10)
print("GET LAST TIME: "),
lastTimeHexStr = child.before.decode().replace(" ","")
print(lastTimeHexStr)
lastTimeMillis = hexStrToInt(lastTimeHexStr)
print("last time "+intToTimeStr(lastTimeMillis))

### setup for bulk read
print("setup for bulk read")
child.sendline("char-write-req 0x001f 0100")
child.expect("Characteristic value was written successfully\r\n", timeout=10)

### bulk read values
readStartTimeMs = curTime - (60 * 10)
readStartTimeHexStr = intToHexStr(readStartTimeMs) 
print("bulk read values...")
cmd = "char-write-req 0x001c "+readStartTimeHexStr
#cmd = "char-write-req 0x001c 00000000"
#cmd = "char-write-req 0x001c 3478a061"
#cmd = "char-write-req 0x001c "+lastTimeHexStr
print(cmd)
child.sendline(cmd)
child.expect("Characteristic value was written successfully\r\n", timeout=10)

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
    break 

  if values[0:8] == "ffffffff":
    print("stop token")
    found_stop = True
    break

  sample_time = hexStrToInt(values[0:8])
  samples = hexStrToSamples(values[8:])

  #print("sample time = "+intToTimeStr(sample_time))
  for j in range(0,len(samples)):
    if samples[j] == "ffffffff":
      print("stop token")
      found_stop = True
      break
    stamp="                   "
    if j==0:
      stamp=intToTimeStr(sample_time) 
    hex_str1 = samples[j]
    bin_str1 = format(hexStrToInt(hex_str1), '0>16b')

    hex1 = samples[j][0:8]
    hex2 = samples[j][8:16]

    sample_bs = hexStrToByteArray(hex_str1)
    new_bs = sample_bs
    #new_bs = struct.pack('<2h', *struct.unpack('>2h', sample_bs))
    h_float = byteArrayToHumidity(new_bs)
    hum_str = "{:>6.2f}".format(h_float)

    t_float = byteArrayToTemperature(new_bs)
    tmp_str = "{:>6.2f}".format(t_float)

    timestep = (new_bs[3] & 255) >> 2

    print(stamp+","+str(j)+","+hex_str1+","+hum_str+","+tmp_str+","+str(timestep))


