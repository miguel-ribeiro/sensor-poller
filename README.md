# Sensor-poller
Dynamic sensor gatherer written in Python 2.7.6 for IoT

This projetct allows for dynamic reading of sensors provided the class file to read them, and stores the results in an output file. It is aimed for many prototypes of the same project that can have different sensors attached.

The poller uses information from the modules provided by the user, and the configuration file, that acts as an interface between the modules and the poller. It indicates which classses, and files to load, and which functions to call for each entry of the configuration.

# Config
## config_project.json
Stores the project configurations common to all boxes, such as server url, software version, and polling interval

## config_box.json
Stores the configuration about the box ID, and the individual sensors to poll.

### Fields
Each entry has the following mandatory fields:  
* <b>"name":                         String</b>          - user defined name for the sensor  
* <b>"enabled":                      Boolean</b>         - used to ignore this item or not  
* <b>"description":                  String</b>          - user description about the sensor Ex:"I2C reads: temp, pressure, alt, humid"  
* <b>"input":                        Integer/String</b>  - Input passed as parameter to the constructor of the module used to read the sensor  
* <b>"file_name":                    String</b>          - Name of the file inside the folder "modules" which contains the class with the module_name  
* <b>"module_name": <t>String</b>          - Class name inside the module file that contains the functions to read the file. The initialization receives the argument of the pin to read  
* <b>"properties":               Array</b>            - Indicates which values to read from the sensor and which functions to call to retrieve those values  
  *  {
    *   <b>"name": String</b> user defined name of the value to read (will be used in the output file to identify the values
    *   <b>"function_name": String - the name of the function inside the class to call and retrieve the values</b>  "get_rain_since_last_request",
    *   <b>"return_values": Array[String] - </b>  -- _OPTIONAL_ can receive an optional array of strings with the return values keys when the function to read returns a dictionary with more than one value  
  *   }


### Example
```   
{  
    "box_id": 12345,  
    "sensors": [  
      {  
          "name": "bme280",  
          "enabled": "True",  
          "description": "I2C: temp, pressure, alt, humid",  
          "input": 0,  
          "file_name": "bme280",  
          "module_name": "BME280Reader",  
          "properties":[  
              {"name": "temperature",  "function_name": "get_temperature"},  
              {"name": "air_pressure", "function_name": "get_pressure"},  
              {"name": "altitude",     "function_name": "get_altitude"},  
              {"name": "humidity",     "function_name": "get_humidity"}  
          ]  
      },  
      {  
          "name": "rain",  
          "enabled": "True",  
          "description": "interrupt rain",  
          "input": 6,  
          "file_name": "rain",  
          "module_name": "RainReader",  
          "properties":[  
              {"name": "rain", "function_name": "get_rain_since_last_request", "return_values":["rain", "nr_ticks"]}  
          ]  
      }  
}   
```


# Advantages
*  This allows to read multiple sensors in a single script, which is dinamycally fed by the contents of the config file.
*  Updates to the modules can be made without having to modify the keys, names or import files of the reading script.

----------
Tested on IntelEdison for Iot


--------------
TODO: Send data over network. Manage backup files when no network is present.
