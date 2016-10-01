import requests
import time

while True:
    r = requests.get('http://192.168.0.42:8000/get_settings/10')
    headers = str(r.headers)
    with open('/home/pi/API_test.txt', 'w') as outfile:
		outfile.write(headers)
    time.sleep(1800)
