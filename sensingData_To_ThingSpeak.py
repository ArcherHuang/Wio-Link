
import time 
import httplib, urllib
import json

ApiKey = ""
wioLink_access_token = ""

def post_to_thingspeak(payload):
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    not_connected = 1
    while (not_connected):
        try:
            conn = httplib.HTTPConnection("api.thingspeak.com:80")
            conn.connect()
            not_connected = 0
        except (httplib.HTTPException, socket.error) as ex:
            print "Error: %s" % ex
            time.sleep(10)  # sleep 10 seconds

    conn.request("POST", "/update", payload, headers)
    response = conn.getresponse()
    print( response.status, response.reason, payload, time.strftime("%c"))
    data = response.read()
    conn.close()

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
        params = urllib.urlencode({'field1': data['moisture'], 'key': ApiKey})
        post_to_thingspeak(params)
    time.sleep(10)
