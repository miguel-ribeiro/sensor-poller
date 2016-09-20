import time
import sys
import signal
import atexit
import pyupm_gas as TP401

class AirReader:
	def __init__(self, pin_air_sensor=0):#, value, ppm):
		self.pin_air_sensor = pin_air_sensor
		self.TP401 = TP401.TP401(pin_air_sensor)
		self.WARMUP_MINUTES = 3
		print 'Waiting ' + str(self.WARMUP_MINUTES) + ' minutes for warm up the sensor'
		for i in range (self.WARMUP_MINUTES):
			time.sleep(1)
			print str(i + 1) + " minute(s) passed."
		print "Sensor is Ready"


	# Give a qualitative meaning to the value from the sensor
	def airQualityDescription(self, value):
		if(value < 50): 
			return "Fresh Air"
		if(value < 200): 
			return "Normal Indoor Air"
		if(value < 400): 
			return "Low Pollution"
		if(value < 600): 
			return "High Pollution - Action Recommended"
		return "Very High Pollution - Take Action Immediately"
	
	def getAirQualityIndex(self):
		raw_value = self.TP401.getSample()
		description = self.airQualityDescription(raw_value)
		return {'raw': raw_value, 'description': description}

	def getPPM(self):
		return round(self.TP401.getPPM(), 3)		# CO (carbon monoxide) parts per million (if > 35 is toxic)
		
		
if __name__ == "__main__":
	pin_air_sensor = 0

	if (len(sys.argv) == 2):
		try:
			pin_air_sensor = int(sys.argv[1])
		except ValueError:
			printf("Invalid pin " + sys.argv[1])
			
	air_reader = AirReader(pin_air_sensor)#, value, ppm)
	# Loop indefinitely
	while True:

		# Read values (consecutive reads might vary slightly)
		value = air_reader.getAirQualityIndex()['raw']
		description = air_reader.getAirQualityIndex()['description']
		ppm = air_reader.getPPM()

		print "raw: %4d" % value , description, " ppm: %5.2f   " % ppm
		# Sleep for 2.5 s
		time.sleep(2.5)
