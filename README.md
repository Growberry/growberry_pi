![Alternate image text](https://github.com/Growberry/growberry_pi/blob/master/growberry_icon_sqare_gimp_125.png)

# growberry_pi
Here is where I will work on code for my raspberry pi controlled growth chamber

This is a collaborative project, and feedback is ALWAYS welcome

## Steps:

    sudo raspi-config

Change the timezone.  Without proper time setting, your pi won't know when to turn the lights on and off.  
Enable camera,
enable ssh (I think this happens by default now.)

    sudo apt-get install vim
    sudo apt-get install git
    sudo apt-get install supervisor
    sudo apt-get install build-essential python-dev
    sudo apt-get install python-virtualenv
    sudo apt-get update
    sudo apt-get upgrade

## Enable 1-wire temp sensors:
Add to bottom of the config file - the <pin#> for my device is 20

    sudo echo "dtoverlay=w1-gpio,gpiopin=<pin#>"  >> /boot/config.txt

You can check that this worked by rebooting the pi, and navigating to `/sys/bus/w1/devices`  There should exist a directory for every w1 therm device connected.  You can check the temps by `cat ./*/w1_slave`

## Clone this repository:

    git clone https://github.com/Growberry/growberry_pi.git
    cd growberry_pi/
    cp supervisor_config.txt /etc/supervisor/supervisor.conf
    
## Make logging into the pi via ssh cooler: (not required)
move message of the day to /etc/ to give custom ssh login welcome message
    
    sudo cp motd /etc/
    
## Make a virtual environment to keep the system python safe

    # old
    virtualenv venv
    
    # new
    python3 venv growberry_pi/venv


## activate the virtual-env

    source /home/pi/growberry_pi/venv/bin/activate

## Install requirements

    pip install -r requirements.txt

## Clone the Adafruit respositories to interface with the 16x2 LCD

    git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git
    cd Adafruit_Python_charLCD/
    sudo python setup.py install

## Clone the Adafruit respositories to interface with the DNT22 temperature/humidity sensor

    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    cd Adafruit_Python_DHT/
    sudo python setup.py install


## Edit your config file to represent your hardware situation

    vi growberry_pi/growberry/config.py

## Notes about getting supervisor to work... This is tricky sometimes.
this works for now (dec 2016)
the file is made according to the docs:
http://supervisord.org/installing.html
but add the [your program name] section:
[program:growberry_pi]
command = python /home/pi/growberry_pi/growberry
directory = /home/pi/growberry_pi/
user = pi
logfile=/var/log/supervisor/supervisord.log
redirect_stderr = True                                                                  
environment = PRODUCTION=1
pay special attention to the log file.  It must be in a supervisor log location.
make the correct path exist:
mkdir /var/log/supervisor/
make sure the owner of the log files match that of the <user=> section of the conf file
sudo chown youuser:youuser -R /var/log/supervisor/
modify permissions on supervisord.conf
section under [unix_http_server]
chmod = 0766  (the default is 0700)
once changed, do a sudo reboot to make the changes take effect
enter supervisorctl, and start the process:
sudo supervisorctl
reread
update

## Reboot the pi.  Supervisor should start the growberry process

    sudo apt reboot



