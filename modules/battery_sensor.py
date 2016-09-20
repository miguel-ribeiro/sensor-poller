import time
import datetime
from os import popen
import mraa
import sys

class BatteryReader:

	def __init__(self, pin_reader=2):
		self.pin_reader = pin_reader
		
		try:
			self.analog_input = mraa.Aio(self.pin_reader)
		except ValueError as e:
			print(e)

	def get_battery_information(self):
		adc_bat = self.analog_input.read()			 # get the current reading from the sensor
		value_batt = adc_bat / 1023.0 * 5.0 		 # converts adc value 0-1023 to Volts  

		batteryObj = {
			"voltage": round(value_batt, 3),
			"percent": self.voltage_to_percentage(value_batt)	 # converts Volts to percentage
		}
		return batteryObj

	def get_num(x):
		return int(''.join(ele for ele in x if ele.isdigit()))
		
	def voltage_to_percentage(self, val_batt):
		percentages_arr = [
			{'v': 3.802, 'p': 100},
			{'v': 3.788, 'p': 99},
			{'v': 3.798, 'p': 98},
			{'v': 3.799, 'p': 97},
			{'v': 3.781, 'p': 96},
			{'v': 3.778, 'p': 95},
			{'v': 3.767, 'p': 94},
			{'v': 3.756, 'p': 93},
			{'v': 3.737, 'p': 92},
			{'v': 3.737, 'p': 91},
			{'v': 3.728, 'p': 90},
			{'v': 3.718, 'p': 89},
			{'v': 3.716, 'p': 88},
			{'v': 3.697, 'p': 87},
			{'v': 3.689, 'p': 86},
			{'v': 3.672, 'p': 85},
			{'v': 3.662, 'p': 84},
			{'v': 3.668, 'p': 83},
			{'v': 3.661, 'p': 82},
			{'v': 3.652, 'p': 81},
			{'v': 3.639, 'p': 80},
			{'v': 3.627, 'p': 79},
			{'v': 3.617, 'p': 78},
			{'v': 3.616, 'p': 77},
			{'v': 3.611, 'p': 76},
			{'v': 3.603, 'p': 75},
			{'v': 3.595, 'p': 74},
			{'v': 3.584, 'p': 73},
			{'v': 3.578, 'p': 72},
			{'v': 3.566, 'p': 71},
			{'v': 3.561, 'p': 70},
			{'v': 3.549, 'p': 69},
			{'v': 3.543, 'p': 68},
			{'v': 3.539, 'p': 67},
			{'v': 3.538, 'p': 66},
			{'v': 3.519, 'p': 65},
			{'v': 3.51, 'p': 64},
			{'v': 3.513, 'p': 63},
			{'v': 3.502, 'p': 62},
			{'v': 3.495, 'p': 61},
			{'v': 3.483, 'p': 60},
			{'v': 3.472, 'p': 59},
			{'v': 3.466, 'p': 58},
			{'v': 3.463, 'p': 57},
			{'v': 3.459, 'p': 56},
			{'v': 3.461, 'p': 55},
			{'v': 3.451, 'p': 54},
			{'v': 3.439, 'p': 53},
			{'v': 3.444, 'p': 52},
			{'v': 3.44, 'p': 51},
			{'v': 3.427, 'p': 50},
			{'v': 3.408, 'p': 49},
			{'v': 3.423, 'p': 48},
			{'v': 3.417, 'p': 47},
			{'v': 3.404, 'p': 46},
			{'v': 3.404, 'p': 45},
			{'v': 3.405, 'p': 44},
			{'v': 3.402, 'p': 43},
			{'v': 3.39, 'p': 42},
			{'v': 3.396, 'p': 41},
			{'v': 3.394, 'p': 40},
			{'v': 3.396, 'p': 39},
			{'v': 3.399, 'p': 38},
			{'v': 3.387, 'p': 37},
			{'v': 3.381, 'p': 36},
			{'v': 3.36, 'p': 35},
			{'v': 3.365, 'p': 34},
			{'v': 3.362, 'p': 33},
			{'v': 3.352, 'p': 32},
			{'v': 3.353, 'p': 31},
			{'v': 3.352, 'p': 30},
			{'v': 3.333, 'p': 29},
			{'v': 3.331, 'p': 28},
			{'v': 3.306, 'p': 27},
			{'v': 3.283, 'p': 26},
			{'v': 3.287, 'p': 25},
			{'v': 3.292, 'p': 24},
			{'v': 3.282, 'p': 23},
			{'v': 3.249, 'p': 22},
			{'v': 3.255, 'p': 21},
			{'v': 3.251, 'p': 20},
			{'v': 3.231, 'p': 19},
			{'v': 3.233, 'p': 18},
			{'v': 3.23, 'p': 17},
			{'v': 3.206, 'p': 16},
			{'v': 3.204, 'p': 15},
			{'v': 3.19, 'p': 14},
			{'v': 3.175, 'p': 13},
			{'v': 3.157, 'p': 12},
			{'v': 3.155, 'p': 11},
			{'v': 3.138, 'p': 10},
			{'v': 3.108, 'p': 9},
			{'v': 3.107, 'p': 8},
			{'v': 3.81, 'p': 7},
			{'v': 3.63, 'p': 6},
			{'v': 3.35, 'p': 5},
			{'v': 2.939, 'p': 4},
			{'v': 2.878, 'p': 3},
			{'v': 2.757, 'p': 2},
			{'v': 2.659, 'p': 1},
			{'v': 2.417, 'p': 0}
		]
		
		for item in percentages_arr:
			if(val_batt >= item['v']):
				return item['p']
		return 0
	
if __name__ == "__main__":
	pin_reader = 2
	if (len(sys.argv) == 2):
		try:
			pin_reader = int(sys.argv[1])
		except ValueError:
			printf("Invalid pin " + sys.argv[1])
			
	batery_reader = BatteryReader(pin_reader)
	print batery_reader.voltage_to_percentage(3.5)

	while True:
		print batery_reader.get_battery_information()
		
		
		
		#v = popen("battery-voltage").read() #.replace('\n', ',')
		#lines = v.splitlines()
		
		#voltage = get_num(lines[0])
		#percent = get_num(lines[1])
		#adc_raw = analog_input.read()
		#adc_vBatt = adc_raw / 1023.0 * 5.0
		# d = datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S')
		# print d, 'voltage', voltage, 'percent', percent, 'adc_raw', str(adc_raw), 'adc_vBatt', str(adc_vBatt)

		# with open("powerTest5-60seg.log", 'a') as log_file:
			# log_file.write(str(d) + ',' + str(voltage) + ',' + str(percent) + ',' + str(adc_raw) + ',' + str(adc_vBatt) + '\n')
		time.sleep(10)
		
		
