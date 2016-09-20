import time
import sys
import signal
import atexit
import pyupm_bmp280 as upm_bme280

class BME280Reader:
	def __init__(self, bus_number):
		self.bus_number = bus_number
		self.upm_bme280 = upm_bme280.BME280(bus_number)
		
	#def get_rain_since_last_request(self):
	#	rain_reader_helper.lock_counter.acquire()
	#	rain_value = rain_reader_helper.rain_counter * self.calibration
	#	rain_reader_helper.rain_counter = 0
	#	rain_reader_helper.lock_counter.release()
		
	#	return rain_value
	
	def update(self):
	 	self.upm_bme280.update()

	def get_temperature(self, farenheight=False):
		self.upm_bme280.update()
		return round(self.upm_bme280.getTemperature(farenheight), 2)

	def get_pressure(self):
		self.upm_bme280.update()
		return round(self.upm_bme280.getPressure(), 3)

	def get_altitude(self):
		self.upm_bme280.update()
		return round(self.upm_bme280.getAltitude())

	def get_humidity(self):
		self.upm_bme280.update()
		return round(self.upm_bme280.getHumidity(), 1)


#o import não influencia o main
if __name__ == "__main__":
	# Instantiate a BME280 instance using default i2c bus and address
	bme280_reader = BME280Reader(0)

	while (1):
		bme280_reader.update()

		print "Compensation Temperature:", bme280_reader.getTemperature(), "C /",
		print bme280_reader.getTemperature(True), "F"

		print "Pressure: ", bme280_reader.getPressure(), "Pa"

		print "Computed Altitude:", bme280_reader.getAltitude(), "m"

		print "Humidity:", bme280_reader.getHumidity(), "%RH"

		print
		time.sleep(1)
