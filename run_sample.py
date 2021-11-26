import sensor

sensor.connect()

v,t = sensor.read_batt_info()
print("Battery info: volts={:>6.2f} raw temp={:>6.2f}".format(v,t))

rev_code_str = sensor.read_revision_code()
print("Revision code: {}".format(rev_code_str))

dev_id_int = sensor.read_device_id()
print("Device id: {}".format(dev_id_int))

samp_intv_secs = sensor.read_sample_interval()
print("Sample interval: {}".format(samp_intv_secs))

