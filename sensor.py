import pexpect
import utils as ut

# change this to your sensor address
# use hcitool to find it:
#   sudo hcitool lescan
#
DEFAULT_SENSOR_ADDR="A4:34:F1:7F:CD:D8"

HND_BATT_INFO = "0x0018"
HND_TIMESTAMP = "0x1a"
HND_SAMPLE_INTERVAL = "0x0014"
HND_REVISION_CODE = "0x0010"
HND_DEVICE_ID = "0x000e"
HND_BULK_READ = "0x001c"
HND_ADV_INTERVAL = "0x0016"
HND_WRITE_NOTIFY = "0x001e"

RESPONSE_WRITE_SUCCESS = "Characteristic value was written successfully\r\n"
RESPONSE_READ_SUCCESS = "Characteristic value/descriptor: "

TIMEOUT=10

child=pexpect.spawn("gatttool -I")

def connect(addr = DEFAULT_SENSOR_ADDR):
  print("Connecting to "+addr+"..."),
  child.sendline("connect {0}".format(addr))
  child.expect("Connection successful", timeout=10)
  return

def read_hnd(hnd):
  child.sendline("char-read-hnd "+hnd)
  child.expect(RESPONSE_READ_SUCCESS, timeout=TIMEOUT)
  child.expect("\r\n", timeout=TIMEOUT)
  hex_str = child.before.decode().replace(" ","")
  return hex_str

def write_req(hnd, val):
  child.sendline("char-write-req "+hnd+" "+val)
  child.expect(RESPONSE_WRITE_SUCCESS, timeout=TIMEOUT)
  return

def read_batt_info():
  hexStr = read_hnd(HND_BATT_INFO)
  voltHex = hexStr[0:4]
  tempHex = hexStr[4:8]
  volts = ut.hexStrToInt(voltHex) / 1000
  rawTemp = ut.hexStrToInt(tempHex)
  return volts, rawTemp

def write_timestamp(hex_str):
  write_req(HND_TIMESTAMP, hex_str)
  return

def read_timestamp():
  return read_hnd(HND_TIMESTAMP)

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

def read_sample_interval():
  hex_str = read_hnd(HND_SAMPLE_INTERVAL)
  return ut.hexStrToInt(hex_str)


