# *******************************************************************************************

# *******************************************************************************************

import time 
import httplib, urllib
import json
import datetime
import requests

DeviceID = ""
wioLink_access_token = "6b186b35b03cf3f1f17b9c09b93c094b"

# ******************************************************************************************
# Set Firebase URL, Date, Time, Location                                                   #                                                                         #
# ******************************************************************************************

firebase_url = 'https://.firebaseio.com/'
temperature_location = 'Taipei';
t = time.time();
date = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')

while True:
    conn = httplib.HTTPSConnection("us.wio.seeed.io", 443)
    conn.request("GET", "/v1/node/GroveMoistureA0/moisture?access_token=" + wioLink_access_token)
    r1 = conn.getresponse()
    print r1.status, r1.reason
    if r1.status == 200:	
        data1 = r1.read()
        print data1
        data = json.loads(data1)
        print "moisture: ", data['moisture']

        # ******************************************************************************************
        # Insert Data                                                                              #
        # ******************************************************************************************    

        data = {'date':date,'moisture':data['moisture']}
        result = requests.post(firebase_url + '/' + temperature_location + '/moisture.json', data=json.dumps(data))
        print 'Status Code = ' + str(result.status_code) + ', Response = ' + result.text

    time.sleep(10)
