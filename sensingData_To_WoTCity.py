# *******************************************************************************************
# 1. install setuptools
#    curl https://bootstrap.pypa.io/ez_setup.py -k -o - | python
#
# 2. install six
#    wget --no-check-certificate https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz
#    tar zxvf six-1.10.0.tar.gz
#    cd six-1.10.0
#    python setup.py install
#
# 3. install Websocket
#    wget --no-check-certificate https://pypi.python.org/packages/source/w/websocket-client/websocket_client-0.32.0.tar.gz
#    tar zxvf websocket_client-0.32.0.tar.gz
#    cd websocket_client-0.32.0
#    python setup.py install
# *******************************************************************************************

import time 
import httplib, urllib
import json
import websocket
import datetime

DeviceID = ""
wioLink_access_token = ""

websocket.enableTrace(True)
ws = websocket.create_connection("ws://wot.city/object/" + DeviceID + "/send")

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
        t = time.time();
        date = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')
        vals = "{\"date\":\""+date+"\",\"moisture\":"+ str(data['moisture'])+"}"
        ws.send(vals);
        print vals;
    time.sleep(10)
