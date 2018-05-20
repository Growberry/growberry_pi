import json
import requests
import datetime
import logging

logger = logging.getLogger(__name__)

class Settings(object):
    """
    class to hold all settings. Can get/update settings. Returns settings in correct object way
    This probably shouldn't exist, and this should just part of the __main__, but it helps me keep things straight.
    if running in "ofline" mode, the settings can be set by manually editing settings.json
    """
    def __init__(self, base_url, file_loc, grow_id):
        self.file_loc = file_loc  # the settings are written memory as json allow usage when offline
        self.grow_id = str(grow_id)  # Database ID
        self.url = base_url + self.grow_id
        self.settings = {}  # store the json as a dictionary for easy python usage
        self.online = False
        self.startdate = None
        self.daylength = None
        # self.pic_dir = None
        self.settemp = None
        self.sethumid = None
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
            logger.info('Settings retrieved from growberry_web: {}'.format(r.text))
        except Exception as e:  # catch all errors, and repor them
            self.settings.update({'online':False, 'error':e})  # add the error to settings.json, and flag it as offline
            logger.warning('Settings could not be obtained from growberry_web: {}'.format(e))
        finally:  # even if the device is offline, it will read the local settings.json
            try:
                with open(self.file_loc, 'r') as infile:
                    self.settings.update(json.load(infile))
                    self.startdate = datetime.datetime.strptime(self.settings.get('startdate', '042016'),'%m%d%y')
                    self.sunrise = datetime.datetime.strptime(self.settings['sunrise'],'%H%M').time()
                    self.daylength = datetime.timedelta(hours=float(self.settings['daylength']))
                    # self.pic_dir = self.settings.get('pic_dir', '/fake/pic_dir/')
                    self.settemp = float(self.settings.get('settemp', 25))  # check for a 'settemp' in the settings, if none, use 25
                    self.sethumid = float(self.settings.get('sethumid', 75))  # check for a 'sethumid' in the settings, if none, use 75
                logger.debug('settings.json sucessfully loaded.')
            except Exception as e:
                logger.critical('settings.json could not be loaded: {}'.format(e))


if __name__ == '__main__':
    test_grow_id = input('what grow number do you want to test?\n>>>')
    fl = 'settings.json'
    test_url = input('which server do you want to check? \n(local/web)>>>')
    if test_url == 'local':
        url = 'http://localhost:5000/get_settings/'
    elif test_url == 'web':
        url = 'http://192.168.0.42:8000/get_settings/'
    settings = Settings(url, fl, test_grow_id)

    settings.update()
    print(settings.settings)
    print(settings.startdate)
    print(settings.sunrise)
    print(type(settings.sunrise))
    print(settings.daylength)
