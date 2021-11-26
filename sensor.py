import pexpect
import utils as ut

# change this to your sensor address
# use hcitool to find it:
#   sudo hcitool lescan
#
DEFAULT_SENSOR_ADDR="A4:34:F1:7F:CD:D8"

HND_BATT_INFO = "0x0018"
HND_TIMESTAMP = "0x1a"
HND_SAMPLE_INTERVAL = ""
HND_REVISION_CODE = "0x0010"
HND_DEVICE_ID = "0x000e"
HND_BULK_READ = "0x001c"
HND_ADV_INTERVAL = "0x0016"
HND_WRITE_NOTIFY = "0x001e"

HND_UNKNOWN1 = "0x0014"

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


