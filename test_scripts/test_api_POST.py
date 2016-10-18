import requests
import time
import json
import random

url = 'http://192.168.0.42:8000/reading/2'
f = "post.log"
temp = 99.0
humidity = 99.0
headers = {'Content-Type': 'application/json',}

while True:

    # these are the fields that are needed for the Reading database table
    dd = {'internal_temp': str(temp), 'internal_humidity': str(humidity), 'pic_dir': '/User/pi/pictures/1.jpg'}
    data = json.dumps(dd)
    r = requests.post(url, headers=headers, data=data)
    returned_headers = str(r.headers)
    with open(f, 'a') as outfile:
        outfile.write(returned_headers)
        outfile.write("\n")
    #make the temps and humidity fluctuate:
    temp += random.uniform(-2,2)
    humidity += random.uniform(-5,5)
    #attempt to call the api every half hour
    time.sleep(1800)
