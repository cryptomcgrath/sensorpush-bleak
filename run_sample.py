import sensor
import utils as ut
import numpy
import sensorpush

sensor.connect()

v,t = sensor.read_batt_info()
print("Battery info: volts={:>6.2f} raw temp={:>6.2f}".format(v,t))

rev_code_str = sensor.read_revision_code()
print("Revision code: {}".format(rev_code_str))

dev_id_int = sensor.read_device_id()
print("Device id: {}".format(dev_id_int))

samp_intv_secs = sensor.read_sample_interval()
print("Sample interval: {}".format(samp_intv_secs))

last_time = sensor.read_timestamp()
print("Last timestamp: {}".format(ut.intToTimeStr(last_time)))

def notify_data(sample_time, samples, rawbytes):
  degree_sign = u"\N{DEGREE SIGN}"
  stamp=ut.intToTimeStr(sample_time)

  for j in range(0,len(samples)):
    s=""
    if j==0:
      s = stamp
    sample_bytes = ut.hexStrToBytes(samples[j][0:8])
    ## add dummy byte to beginning
    sample_bytes = bytearray([65])+sample_bytes
    vals = sensorpush.decode_values(sample_bytes, 65)
    temp_c = vals["temperature"]
    temp_f = ut.celsiusToFahrenheit(temp_c)
    hum = vals["humidity"]
    print("{:>20},{},temp: {:>7.3f}{}f ({:>7.3f}{}c) hum: {:>7.3f}%".format(s, samples[j], temp_f, degree_sign, temp_c, degree_sign, hum))

read_start_time_hex = ut.intToHexStr(last_time-(60*30))
sensor.read_bulk_values(read_start_time_hex, notify_data)

