import mraa
import time
import sys
from threading import Lock

class WindSpeedReader:
	def __init__(self, pin_number):
		wind_speed_helper.initialize(pin_number)
		
	def get_wind_speed_since_last_request(self):
		wind_speed_helper.lock_counter.acquire()
		wind_speed_helper.deltaTime = (time.time() - wind_speed_helper.lastWindCheck)
		wind_speed_helper.lastWindCheck = time.time()
		#wind_speed_helper.deltaTime *= 1000.0; #Covert to seconds
		#print "last wind check:" + str(wind_speed_helper.deltaTime)

		wind_nr_ticks = wind_speed_helper.wind_ticks
		wind_clicks_per_second = wind_speed_helper.wind_ticks / wind_speed_helper.deltaTime; 	# 3 / 0.750s = 4
		wind_speed_helper.wind_ticks = 0; 														# Reset and start watching for new wind
		wind_speed_value = wind_clicks_per_second * 2.4 * 0.277777778							# speed in meters per secons (m/s)
		wind_speed_helper.lock_counter.release()
		
		return {'wind': round(wind_speed_value, 3), 'nr_ticks': wind_nr_ticks}
		
def speed_IRQ(self):
	wind_speed_helper._speed_IRQ()
 
class _WindSpeedReader:
	def initialize(self, pin_number=5):
		self.pin_number = pin_number
		self.lock_counter = Lock()
		
		self.lock_counter.acquire()
		self.wind_ticks = 0
		self.lastWindCheck = 0
		self.lastWindCheck = 0
		self.lock_counter.release()
		
		#print("Starting ISR for pin " + repr(pin))		
		self.value_input = mraa.Gpio(pin_number)
		self.value_input.dir(mraa.DIR_IN)
		self.value_input.isr(mraa.EDGE_RISING, speed_IRQ, self.value_input)
		
	def _speed_IRQ(self):
		self.lock_counter.acquire()
		self.wind_ticks += 1	
		#print "Current count: " + str(self.wind_ticks)
		self.lock_counter.release()
  
wind_speed_helper = _WindSpeedReader()
  
## Exit handlers ## le o ctrl_c
def SIGINTHandler(signum, frame):
	global thread_exit
	thread_exit = True
	raise SystemExit
	
	## Exit handlers ## le o ctrl_c
def SIGTSTPHandler(signum, frame):
	global thread_exit
	thread_exit = True
	print "exiting thread true"
	raise SystemExit

def exitHandler():
	print "Exiting"
	thread_exit = True
	sys.exit(0)

if __name__ == "__main__":
	READ_PIN = 5;
	if (len(sys.argv) == 2):
	  try:
		READ_PIN = int(sys.argv[1])
	  except ValueError:
		printf("Invalid pin " + sys.argv[1])
		
	speed_reader = WindSpeedReader(READ_PIN)	
	
	while True:
		wind_speed = speed_reader.get_wind_speed_since_last_request()
		print wind_speed['wind'], wind_speed['nr_ticks']
		time.sleep(1)
		