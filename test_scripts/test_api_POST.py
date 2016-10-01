import requests
import time
import json
import random

f = "post.log"
temp = 20.0
humidity = 50.0
random.uniform(1, 10)
while True:

    headers = {'Content-Type': 'application/json',}
    # these are the fields that are needed for the Reading database table
    dd = {'internal_temp': str(temp), 'internal_humidity': str(humidity), 'pic_dir': '/User/pi/pictures/1.jpg'}
    data = json.dumps(dd)
    r = requests.post('http://localhost:5000/reading/1', headers=headers, data=data)
    headers = str(r.headers)
    with open(f, 'w+') as outfile:
        outfile.write(headers)
    #make the temps and humidity fluctuate:
    temp += random.uniform(-2,2)
    humidity += random.uniform(-5,5)
    #attempt to call the api every half hour
    time.sleep(1800)
