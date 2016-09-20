import time
import sys
import signal
import atexit
import pyupm_si114x as upmSi114x

class UVReader():
	def __init__(self, pin_number=1):
		self.pin_number = pin_number
		self.myUVSensor = upmSi114x.SI114X(pin_number)
		self.myUVSensor.initialize()

	def get_uv_index(self):
		self.myUVSensor.update()
		return round(self.myUVSensor.getUVIndex(), 3)

#o import não influencia o main
if __name__ == "__main__":
	#Instantiate a SI114x UV Sensor on I2C bus 1
	uv_reader = UVReader(1)

	# uv_reader.initialize()

	print "UV Index Scale:"
	print "---------------"
	print "11+        Extreme"
	print "8-10       Very High"
	print "6-7        High"
	print "3-5        Moderate"
	print "0-2        Low\n"

	# update every second and print the currently measured UV Index
	while (1):
		# update current value(s)
		# uv_reader.update()

		# print detected value
		print "UV Index:", uv_reader.get_uv_index()

		time.sleep(1)




