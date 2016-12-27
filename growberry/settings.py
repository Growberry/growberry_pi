import json
import requests
from datetime import datetime, timedelta 
import logging

logger = logging.getLogger(__name__)

class Settings(object):
    """class to hold all settings. Can get/update settings. Returns settings in correct object way"""
    def __init__(self,base_url,file_loc, grow_id):
        self.file_loc = file_loc
        self.grow_id = str(grow_id)
        self.url = base_url + self.grow_id
        self.settings = {}
        self.online = False
        self.startdate = None
        self.daylength = None
        self.pic_dir = None
        self.settemp = None
        logger.info('Settings instance created.')

    def update(self):
        try:
            # if connected to the internet, request settings
            r = requests.get(self.url)
            settings_json = r.json()   #json.loads(r.text)
            # set attributes 'online' and 'error'
            settings_json['online'] = True
            settings_json['error'] = False
            with open(self.file_loc,'w') as f:
                json.dump(settings_json,f)
            logger.info('Settings retrieved from growberry_web: %s' % r.text)
        except Exception,e:
            error = {'online':False, 'error':e}
            self.settings.update(error)
            logger.warning('Settings could not be obtained from growberry_web: %s' % e)
        finally:
            try:
                with open(self.file_loc, 'r') as infile:
                    self.settings.update(json.load(infile))
                    self.startdate = datetime.strptime(self.settings.get('startdate', '042016'),'%m%d%y')
                    self.sunrise = datetime.strptime(self.settings['sunrise'],'%H%M').time()
                    self.daylength = timedelta(hours=float(self.settings['daylength']))
                    self.pic_dir = self.settings.get('pic_dir', '/fake/pic_dir/')
                    self.settemp = float(self.settings.get('settemp', 25))
                logger.debug('settings.json sucessfully loaded.')
            except Exception,e:
                logger.critical('settings.json could not be loaded: %s' %e)


if __name__ == '__main__':
    test_grow_id = 2
    test_url = 'http://localhost:5000/get_settings/'
    test_url2 = 'http://ec2-54-244-205-179.us-west-2.compute.amazonaws.com/get_settings/'
    fl = 'settings.json'
    settings = Settings(test_url2,fl,test_grow_id)

    settings.update()
    print settings.settings
    print settings.startdate
    print settings.sunrise
    print settings.daylength
