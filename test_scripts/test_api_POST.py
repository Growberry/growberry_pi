import requests
import time
import json
import random
import datetime

# url = 'http://127.0.0.1:5000/reading/3'
# url = 'http://192.168.0.42:8000/reading/3'
url = 'http://ec2-54-244-205-179.us-west-2.compute.amazonaws.com/reading/'

f = "post.log"
headers = {'Content-Type': 'application/json',}

testdata = {'fanspeed': 29.6,
            'timestamp': datetime.datetime(2016, 11, 19, 7, 26, 35, 240908).isoformat(),
            'lights': 1,
            'pic_dir':'fake',
            'sinktemps': [16.937, 17.437, 16.687, 17.187, 16.687, 17.437],
            'sensors': {'internal': {'timestamp': datetime.datetime(2016, 11, 19, 7, 26, 34, 715252).isoformat(),
 			 			'temp': 14.8,
 			 			'humidity': 59.7
 			 			            },
 			 	        'external': {'timestamp': datetime.datetime(2016, 11, 19, 7, 26, 35, 240868).isoformat(),
 			 			'temp': 17.2,
 			 			'humidity': 48.9
 			 			            }
 			 	        },

            }

while True:

    # these are the fields that are needed for the Reading database table
    # dd = {'internal_temp': str(temp), 'internal_humidity': str(humidity), 'pic_dir': '/User/pi/pictures/1.jpg'}
    data = json.dumps(testdata)
    r = requests.post(url, headers=headers, data=data)  #data
    returned_headers = str(r.headers)
    print 'returned: ',r, 'of type: ', type(r)
    print '\nthe tex of which is: ', r.text

    # with open(f, 'a') as outfile:
    #     outfile.write(returned_headers)
    #     outfile.write("\n")
    #make the temps and humidity fluctuate:

    temp += random.uniform(-2,2)
    humidity += random.uniform(-5,5)
    #attempt to call the api every half hour
    time.sleep(1800)
