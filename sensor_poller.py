import atexit
import datetime
import importlib
import json
import os
import sys
import signal
import time

from configuration import Configuration

print 'imports done'
# ####################################################

CONF_PROJECT_FILENAME   = 'config/config_project.json'
CONF_BOX_FILENAME       = 'config/config_box.json'
BACKUP_FILENAME         = 'backup_meteo.json'
MODULES_PATH            = 'modules'
LOG_PATH                = 'logs'

# ----------------------------- Exit handlers --------------------------------
# This function stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
    raise SystemExit

# This function lets you run code on exit
def exitHandler():
    print "Exiting"
    sys.exit(0)

# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

# ----------------------------------------------------------
def callMethod(o, name):
    return getattr(o, name)()

def initialize_sensors(sensors):
    for sensorConfig in config.sensors:
        try:
            print sensorConfig['file_name'], sensorConfig['module_name'], sensorConfig['enabled']

            if sensorConfig['enabled']:
                sensor = {}
                sensor['file'] = importlib.import_module(MODULES_PATH + '.' + sensorConfig['file_name'])
                sensor['module'] = getattr(sensor['file'], sensorConfig['module_name'])
                sensor['module'] = sensor['module'](sensorConfig['input'])
                sensor['properties'] = sensorConfig['properties']
                sensors.append(sensor)
        except:
            print "----------------------"
            print "Error importing module - " + sensorConfig['file_name']
            print "----------------------"

def get_date_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') 
        
def get_all_sensor_values(sensors):
    return_values = {}

    for sensor in sensors:
        for sensor_property in sensor['properties']:
            try:
                function_name = sensor_property['function_name']
                property_value = callMethod(sensor['module'], function_name)
                if hasattr(sensor_property, 'return_values'):
                    for value_name in sensor_property.return_values:
                        return_values[value_name] = property_value[value_name]()
                else:
                    return_values[sensor_property['name']] = property_value
            except:
                print "error reading " + sensor_property['name']
    return return_values





#################################################
######--------------  MAIN  -------------- ######
################################################# 
config = Configuration(CONF_PROJECT_FILENAME, CONF_BOX_FILENAME)
config.load_config_values()
print config.box_id
print config.sensors
sensors = []
initialize_sensors(sensors)

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

date = get_date_time()
log_filename = 'meteo_' + date.replace(' ', '_').replace(':', '-') + '.log'

while (1):
    #try:
    date = get_date_time()

    all_sensor_values = get_all_sensor_values(sensors)
    all_sensor_values['datetime'] = date

    print '#####################################'
    print json.dumps(all_sensor_values, indent=4)#, sort_keys=True)

    with open(LOG_PATH + '/' + log_filename ,'a') as f:
        f.write(json.dumps(all_sensor_values) + '\n')
    
    time.sleep(config.)
    #except:
    #    print "error somewhere"
