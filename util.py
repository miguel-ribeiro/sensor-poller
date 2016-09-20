#from utrllib.request import urlopen     # for pyhton 3.4
#from utrllib.request import URLError    # for pyhton 3.4
import urllib2                          #2.7
import requests
import json
import jwt
from os import system

#import mycrypt as Crypto

def hasSiteConnection(site, wifi_connection=False):
    if (site.startswith('http://') == False) and (site.startswith('https://') == False):
        site = 'http://' + site
    try:
        response = urllib2.urlopen(site, timeout=5)
        #response = urlopen(site, timeout=5)
        return True
    #except URLError as err: pass       # for pyhton 3.4
    except urllib2.URLError as err:
        system('sudo ifconfig')                     # without this ip doesn't restore after connection is lost
        if not wifi_connection:
            system('dhclient -r eth0')    # without this ip doesn't restore after connection is lost
            system('/etc/init.d/networking restart')    # without this ip doesn't restore after connection is lost
        system('sudo ifconfig')                     # without this ip doesn't restore after connection is lost
        pass

    return False

def hasURLConnection(url):
    if (url.startswith('http://') == False) and (url.startswith('https://') == False):
        site = 'http://' + url

    try:
        response = urllib2.urlopen(url, timeout=5)
        #response = urlopen(site, timeout=5)
        return True
    #except URLError as err: pass       # for pyhton 3.4
    except urllib2.URLError as err:
        return False

def read_json_config(file, key):
    try:
        with open(file) as data_file:   #might throuw error here
            data = json.load(data_file)
            response = data[key]        #might throuw error here
    except:
        print "there was an error reading JSON config"
        return False
    return response

def readSingleNumberFromFile(filename):
    with open(filename, 'r') as f:
        reader = f.readline()
    line = reader.replace("\r", '').replace("\n", '')
    try:
        c = float(line)
    except ValueError: c = 0
    return c

class AverageCounter:
    def __init__(self):
        self.Counter = 0
        self.Sum = 0

    def add(self, value):
        self.Counter += 1
        self.Sum+= value

    def getAverage(self):
        if(self.Counter > 0):
            return self.Sum / self.Counter
        else:
            return 0

    def reset(self):
        self.Counter = 0
        self.Sum = 0

def updateSystemTime():
    system('TZ="Europe/Lisbon"; export TZ')
    system('ntpdate time.nist.gov')


def writeAliveFile(VERSION):
    """
    Just to know if the software is running, cause it doesn't stay in processes, nor services,
    so b deleting this file and waiting a minute, it will appear again, meaning the software is running
    """
    f = open('ALIVE_' + str(VERSION), 'w')
    f.close()

def writeRebootFile():
    """
    Just to know if the software is running, cause it doesn't stay in processes, nor services,
    so b deleting this file and waiting a minute, it will appear again, meaning the software is running
    """
    f = open('REBOOT', 'w')
    f.close()

def write_values_to_backup(jsonString, BACKUP_FILENAME):
    """
    Writes the list of values to a backup file following the CSV standard
    :param valueList: list of values to be added to the file
    :param BACKUP_FILENAME: String containing the name of the backup file
    :type valueList: []
    """

    f = open(BACKUP_FILENAME, 'a')
    f.write(jsonString + '\n')
    f.close()

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def deleteLinesFromFile(filename, lines_to_delete, contents=False):
    try:
        if len(lines_to_delete) > 0:
            line_number = 0
            if contents == False:
                with open(filename,'r') as f:
                    contents = f.readlines()
            with open(filename,'w') as f:
                for row in contents:
                    if not line_number in lines_to_delete:
                        f.write(row)
                    line_number += 1
    except: # file doesn't exist
        return

def checkfileIntegrity(filename):
    try:
        lines_to_delete = []
        line_number = 0
        with open(filename,'r') as f:
            contents = f.readlines()
            for row in contents:
                try:
                    json.loads(row)
                except:
                    lines_to_delete.append(line_number)
                    print("error loading json -> deleting line")
                line_number += 1
        deleteLinesFromFile(filename, lines_to_delete, contents)
    except: # file doesn't exist
        return

def yield_json_from_backup(BACKUP_FILENAME):
    """
    Reads values stored in a json file and returns an iterator.
    This way, the file is only loaded one line at a time into memory. The file can be huge :P
    :return: a generator (yields) with a line at a time from the backupFile
    """

    try:
        checkfileIntegrity(BACKUP_FILENAME)

        with open(BACKUP_FILENAME, 'r') as f:
            for row in f:
                yield row.replace('\r', '').replace('\n', '')
    except:   # no backup file
        return

def yield_chunk_from_backup(BACKUP_FILENAME, chunkSize=500):
    result = []
    try:
        checkfileIntegrity(BACKUP_FILENAME)

        with open(BACKUP_FILENAME, 'r') as f:
            i = 0
            had_rows = False
            for row in f:
                had_rows = True
                result.append(json.loads(row.replace('\r', '').replace('\n', '')))
                if i == chunkSize:
                    i = 0
                    yield result
                i+= 1
            if had_rows:
                yield result
            else:
                return
    except:   # no backup file
        return


def read_json_from_backup(BACKUP_FILENAME):
    """
    Reads values stored in a json file and returns an iterator.
    This way, the file is only loaded one line at a time into memory. The file can be huge :P
    :return: a generator (yields) with a line at a time from the backupFile
    """
    result = []
    try:
        checkfileIntegrity(BACKUP_FILENAME)

        with open(BACKUP_FILENAME, 'r') as f:
            for row in f:
                result.append(row.replace('\r', '').replace('\n', ''))
    except:   # no backup file
        return result
    return result

def upload_data(jsonObj, SERVER_POST_URL, encryption_key=""):
    """
    Uploads value list to web server by POST. The values should be given in the correct order
    :param values: list of values in the order :produced, consumed, timestamp, voltage, consumed2
    :return: Returns True or False accordingly if the upload was successful
    """
    print jsonObj
    if(encryption_key != ""):
        jsonString = json.dumps({"jwt": jwt.encode(jsonObj, encryption_key, algorithm='HS256')})
        #jsonString = Crypto.encrypt(jsonString, encryption_key)
    else:
        jsonString = json.dumps(jsonObj)
        
    try:
        headers = {'Content-type': 'application/json'}
        r = requests.post(SERVER_POST_URL, data=jsonString, headers=headers)
        if r.status_code == requests.codes.ok:
            #print ('SENT')
            return True
        else:
            #print ('NOT SENT')
            #print (jsonString)
            #print (r)
            #print (r.raw)
            return False
    except:
        return False

def delete_backup_file(BACKUP_FILENAME):
    """
    Deletes the backup file (Useful for deleting backup after sending to server
    """
    fd = open(BACKUP_FILENAME,'w')     # erases backup data by opening a new file for writing with the same name
    fd.close()