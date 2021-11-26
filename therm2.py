import sensor

sensor.connect()

v,t = sensor.read_batt_info()
print("battery volts={:>6.2f} raw temp={:>6.2f}".format(v,t))


