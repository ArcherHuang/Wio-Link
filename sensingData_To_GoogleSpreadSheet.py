# *******************************************************************************************
# 1. install gspread
#    pip install gspread oauth2client
# *******************************************************************************************

import time 
import httplib, urllib
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

credentialFile = ".json"
wioLink_access_token = ""

# Uue Credential
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(credentialFile, scope)
client = gspread.authorize(creds)
 
# Set Sheet
sheet = client.open("sensingData").worksheet("Data")

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

        # Write Value
        rowValue = [data['moisture']]
        print(sheet.row_count)
        index = sheet.row_count + 1
        sheet.insert_row(rowValue, index)
    time.sleep(10)
