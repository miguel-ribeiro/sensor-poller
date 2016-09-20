import mraa
import time
import sys
from threading import Lock

class RainReader:
	def __init__(self, pin_number):
		self.calibration = 0.2794
		rain_reader_helper.initialize(pin_number)
		
	def get_rain_since_last_request(self):
		rain_reader_helper.lock_counter.acquire()
		rain_nr_ticks = rain_reader_helper.rain_counter
		rain_value = rain_reader_helper.rain_counter * self.calibration
		rain_reader_helper.rain_counter = 0
		rain_reader_helper.lock_counter.release()
		
		return {'rain': round(rain_value, 3), 'nr_ticks':rain_nr_ticks}
		
def rain_IRQ(self):
    rain_reader_helper._rain_IRQ()

class _RainReader:
	def initialize(self, pin_number=6):
		self.pin_number = pin_number
		self.lock_counter = Lock()
		
		self.lock_counter.acquire()
		self.rain_counter = 0
		self.lock_counter.release()
		
		self.digital_input = mraa.Gpio(pin_number)
		self.digital_input.dir(mraa.DIR_IN)

		self.digital_input.isr(mraa.EDGE_FALLING, rain_IRQ, self.digital_input)
		#print "initializing _RainReader"
		
	def _rain_IRQ(self):
		self.lock_counter.acquire()
		self.rain_counter += 1				#Each dump is 0.011" of water
		#print "Current count: " + str(self.rain_counter)
		self.lock_counter.release()

rain_reader_helper = _RainReader()
  
# Exit handlers ## le o ctrl_c
def SIGINTHandler(signum, frame):
    global thread_exit
    thread_exit = True
    raise SystemExit
    
# Exit handlers ## le o ctrl_c
def SIGTSTPHandler(signum, frame):
    global thread_exit
    thread_exit = True
    #print "exiting thread true"
    raise SystemExit

def exitHandler():
    print "Exiting"
    thread_exit = True
    sys.exit(0)
	
if __name__ == "__main__":
	READING_PIN = 6;
	if (len(sys.argv) == 2):
	  try:
		READING_PIN = int(sys.argv[1])
	  except ValueError:
		printf("Invalid pin " + sys.argv[1])
		
	rain_reader = RainReader(READING_PIN)
	
	while True:
		rain_hour = rain_reader.get_rain_since_last_request()
		print rain_hour['rain'], rain_hour['nr_ticks']
		time.sleep(5)
		
		