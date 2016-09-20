import mraa
import time
import sys

class WindDirectionReader:
	def __init__(self, pin_number=2):
		self.pin_number = pin_number
		
		try:
			self.analog_input = mraa.Aio(self.pin_number)
		except ValueError as e:
			print(e)

	#Returns the instataneous wind speed and tries to avoid reading errors 5 times
	def get_wind_direction(self, numberOfReads=5, ERROR_TRIES_LIMIT=5):
		error_tries_counter = 0
		
		wind_direction_obj = self._try_get_wind_direction_(numberOfReads)
		
		while wind_direction_obj["error"] and error_tries_counter < ERROR_TRIES_LIMIT:	# call the same function recursivelly until a valid value was read assuming it will always end up reading a valid value
			#print "error"
			error_tries_counter +=1
			wind_direction_obj = self._try_get_wind_direction_(numberOfReads)
			
		return wind_direction_obj		
			
	#Returns the instataneous wind speed
	def _try_get_wind_direction_(self, numberOfReads):
		#read the wind direction sensor, return heading in degrees
		sumReads = 0

		#reads 8 values and retrieves the average
		for x in range(numberOfReads):
			sumReads += self.analog_input.read()
		averageValue = sumReads / numberOfReads  	 # get the current reading from the sensor
		valueV = averageValue * 5.0 / 1023.0	     # converts adc value 0-1023 to Volts  
		#print str(valueV)
		windDirectionObj = self.voltage_to_degree(valueV)	 # converts Volts to direction degrees (North = 0)

		return windDirectionObj

	def voltage_to_degree(self, voltage_read):
		datasheetValues = [
			{"degree": 0,   "voltage": 3.84, "threshold": 0.1},
			{"degree": 23,  "voltage": 1.98, "threshold": 0.1},
			{"degree": 45,  "voltage": 2.25, "threshold": 0.1},
			{"degree": 68,  "voltage": 0.41, "threshold": 0.02},
			{"degree": 90,  "voltage": 0.45, "threshold": 0.02},
			{"degree": 113, "voltage": 0.32, "threshold": 0.07},
			{"degree": 135, "voltage": 0.90, "threshold": 0.1},
			{"degree": 158, "voltage": 0.62, "threshold": 0.1},
			{"degree": 180, "voltage": 1.40, "threshold": 0.1},
			{"degree": 203, "voltage": 1.19, "threshold": 0.1},
			{"degree": 225, "voltage": 3.08, "threshold": 0.05},
			{"degree": 248, "voltage": 2.93, "threshold": 0.05},
			{"degree": 270, "voltage": 4.55, "threshold": 0.1},  #voltage adjust 4.62 to 4.55
			{"degree": 293, "voltage": 4.04, "threshold": 0.09},
			{"degree": 315, "voltage": 4.26, "threshold": 0.1},  #voltage adjust 4.78 to 4.26
			{"degree": 338, "voltage": 3.43, "threshold": 0.1}
		]
		
		for item in datasheetValues:
			if self.fuzzyCompare(item["voltage"], voltage_read, item["threshold"]):		# 380 adc
				return {"error":False, "value": item["degree"]}
			
		return {"error":True, "value":0}

	def fuzzyCompare(self, compare_value, value, VARYVALUE):

		if (value > compare_value - VARYVALUE) and (value < compare_value + VARYVALUE):
			return True;
		return False;
	
# Exit handlers ## le o ctrl_c
# def SIGINTHandler(signum, frame):
	# global thread_exit
	# thread_exit = True
	# raise SystemExit
	
	# Exit handlers ## le o ctrl_c
# def SIGTSTPHandler(signum, frame):
	# global thread_exit
	# thread_exit = True
	# print "exiting thread true"
	# raise SystemExit

# def exitHandler():
	# print "Exiting"
	# thread_exit = True
	# sys.exit(0)

if __name__ == "__main__":
	READING_PIN = 2
	if (len(sys.argv) == 2):
		try:
			READING_PIN = int(sys.argv[1])
		except ValueError:
			printf("Invalid pin " + sys.argv[1])
		
	wind_reader = WindDirectionReader(READING_PIN)
	
	while True:
		wind_direction_obj = wind_reader.get_wind_direction()
		if wind_direction_obj["error"]:
			print "Error reading values"
		else:
			print str(wind_direction_obj["value"])
		
		time.sleep(0.5)
	