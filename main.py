#!/usr/bin/env python3
import json
import requests
import sys
from typing import Tuple

if len(sys.argv) <2:
    print("Wrong number of parameter, Please enter an url")

# api-endpoint
endpoint = "https://archive.org/wayback/available?"

location = sys.argv[1]

def parse_responds(resp: dict) -> Tuple[bool,dict]:
    if len(resp['archived_snapshots']) == 0:
        print('[INFO] Website not available @ waybackmachine')
        return False,[]
    closest = resp['archived_snapshots']['closest']
    t_stamp = closest['timestamp']
    url = closest['url']
    orig_url= resp['url']
    print("Got responds for "+orig_url+" snapshot available @: "+url+" for Data: "+t_stamp)
    return True, [orig_url,url,t_stamp]

def save_snapshot(url: str) -> Tuple[bool,dict]:
    r = requests.post('https://pragma.archivelab.org/', data = {'url':'web.de'})
    resp = r.json()
    if len(resp) < 2:
        print('[INFO] Website not available @ waybackmachine')
        return False,[]

# defining a params dict for the parameters to be sent to the API
PARAMS = {'url':location}

# Source: https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
# sending get request and saving the response as response object
try:
    r = requests.get(url = endpoint, params = PARAMS)
#    snap_responds = r.json()
    parse_responds(r.json())
except requests.exceptions.ConnectionError as e:
    print("[ERROR]: We got a connection error for the request to url="+location)
    print(e)
except requests.exceptions.Timeout:
    # Maybe set up for a retry, or continue in a retry loop
    print("[ERROR]: We got a timeout for the request to url="+location)
except requests.exceptions.TooManyRedirects:
    print("[ERROR]: We got to many redirects for the request to url="+location)
except requests.exceptions.RequestException as e:
    print("[ERROR]: We got to many redirects for the request to url="+location)
    # catastrophic error. bail.
    print(e)
    sys.exit(1)

# extracting data in json format


# extracting latitude, longitude and formatted address
# of the first matching location
#latitude = data['results'][0]['geometry']['location']['lat']
#longitude = data['results'][0]['geometry']['location']['lng']
#formatted_address = data['results'][0]['formatted_address']

# printing the output
#print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#      %(latitude, longitude,formatted_address))



#f = open("demofile.txt", "r")
#for x in f:
#  print(x)

