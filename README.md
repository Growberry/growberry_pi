# growberry_pi
Here is where I will work on code for my raspberry pi controlled growth chamber

This is a collaborative project, and feedback is ALWAYS welcome

steps:

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

    # add to bottom of the config file - the <pin#> for my device is 20
    sudo echo "dtoverlay=w1-gpio,gpiopin=<pin#>"  >> /boot/config.txt

    git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git
    cd Adafruit_Python_charLCD/
    sudo python setup.py install
    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    cd Adafruit_Python_DHT/
    sudo python setup.py install

    git clone https://github.com/Growberry/growberry_pi.git
    cd growberry_pi/
    cp supervisor_config.txt /etc/supervisor/supervisor.conf
    # move message of the day to /etc/ to give custom ssh login welcome message
    sudo cp motd /etc/
    # make a virtual environment to keep the system python safe
    virtualenv venv
    # activate the virtual-env
    source /home/pi/growberry_pi/venv/bin/activate
    # install requirements
    pip install -r requirements.txt


    # Edit your config file to represent your hardware situation
    vi growberry_pi/growberry/config.py




