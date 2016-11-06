import requests
import time

writefile = '/Users/austinmeier/Documents/jaiswal/git/growberry_pi/growberry/test_scripts/data.json'

while True:
    r = requests.get('http://192.168.0.42:8000/get_settings/10')
    headers = str(r.headers)
    with open(writefile, 'w') as outfile:
		outfile.write(headers)
    time.sleep(1800)
