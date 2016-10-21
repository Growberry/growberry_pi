import json
import requests
import time

test_grow_id = 2
test_url = 'http://192.168.0.42:8000/get_settings/10'
test_url2 = 'http://ec2-54-244-205-179.us-west-2.compute.amazonaws.com/get_settings/'

class Settings(object):
    """url will be the API location, and file_loc is the location where the .json will be stored"""
    def __init__(self,base_url,file_loc, grow_id):
        self.file_loc = file_loc
        self.grow_id = str(grow_id)
        self.url = base_url + self.grow_id
        # with open(self.file_loc,'r') as infile:
        #     settings = json.load(infile)
        #     for k,v in settings.iteritems():
        #         self.k = v



    def update(self):
        try:
            r = requests.get(self.url)
            settings_json = r.text
        #     print(type(settings_json))
        #     print (settings_json)
        # finally:
        #     print('done')
            with open(self.file_loc,'w') as f:
                json.dump(settings_json,f)
        finally:
            with open(self.file_loc, 'r') as infile:
                settings = json.load(infile)
                for k, v in settings.iteritems():
                    self.k = v
#
# while True:
#     r = requests.get('http://192.168.0.42:8000/get_settings/10')
#     headers = str(r.headers)
#     with open('/home/pi/API_test.txt', 'w') as outfile:
# 		outfile.write(headers)
#     time.sleep(1800)

if __name__ == '__main__':
    settings = Settings(test_url2,'/Users/meiera/Documents/pythoncode/web_dev/templates/settings.json',2)
    settings.update()

    print(settings.daylength)
    # print(settings)
