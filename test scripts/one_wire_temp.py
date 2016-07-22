#!/usr/bin/env python

from datetime import datetime
import os
from threading import Thread
import time



class w1therm:
    def __init__(self):
        self.sensorroot = '/sys/bus/w1/devices/'
        #find all sensors
        self.sensors = open(self.sensorroot + 'w1_bus_master1/w1_master_slaves').read().splitlines()



    def Read(self,id):
        fname = self.sensorroot + id + "/w1_slave"
        if os.path.isfile(fname):  # Sensor id exists?
            with open(fname, "r") as f:
                data = f.readlines()

            if data[0].strip()[-3:] == "YES":  # Make sure sensor is ready & OK
                return {id: float(data[1].split("=")[1]) / 1000}
        else:
            return {id: None}  # Return null when not found or error

    def Retrieve(self, sensor, result):
        result.update(self.Read(sensor))


    def gettemps(self):
        temps = {}
        threads = []
        # We read every sensor in it's own thread; this speeds up the process massively
        # The DS18B20 driver sets the IC in 'read mode', then waits ~750ms, then reads the value; if we do this
        # concurrently we don't have to wait num_sensors x sensor_delay but only 1 x sensor_delay (+ slight overhead)
        # For 4 sensors we go from 3.5~4.0 seconds to 0.8~1.0 seconds

        for s in self.sensors:
            process = Thread(target=self.Retrieve, args=[s,temps])
            process.start()
            threads.append(process)

        for process in threads:
            process.join()
        temps.update({'timestamp':datetime.now())
        return(temps)







if __name__ == "__main__":
    heatsinktemps = w1therm()
    while true:
        print heatsinktemps.gettemps()
        time.sleep(10)