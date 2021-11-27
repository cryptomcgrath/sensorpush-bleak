import binascii
from datetime import datetime
import pytz

# function to transform hex string like "0a cd" into signed integer
def hexStrToInt(hexstr):
  hexstr = hexstr.replace(" ","")
  bs = binascii.unhexlify(hexstr)
  val = int.from_bytes(bs, byteorder='little')
  return val

def hexStrToBytes(hexstr):
  hexstr = hexstr.replace(" ","")
  return bytearray.fromhex(hexstr)

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

def celsiusToFahrenheit(c):
  return c * 1.8 + 32.0
