
import requests
import json

settings = {}

settingsfile = '/Users/austinmeier/Documents/jaiswal/git/growberry_pi/growberry/data.json'

url = 'http://192.168.0.42:8000/get_settings/10'
test_url = 'http://192.168.0.11:8000/get_settings/10'
url2 = 'http://localhost:5000/get_settings/10'

def update_settings():
    r = requests.get(url2)
    with open(settingsfile,'w') as outfile:
        # json.dump(r.text, outfile)
        outfile.write(r.text)

def load_settings():
    with open(settingsfile,'r') as infile:
        settings = json.load(infile)
    # print settings['flower']
    return settings



update_settings()
settings = load_settings()
print type(settings)
# s = json.loads(settings)
# print type(s)
