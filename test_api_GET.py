import requests
import time

while True:
    r = requests.get('http://192.168.0.42:8000/get_settings/10')
    print r.headers
    time.sleep(3)
