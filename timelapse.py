from datetime import datetime, date, time
import os
import time

#PiLapse, originally written by The HatMan
#Note, all of the print lines can be commented out and are not necessary

#Sets time for when the photos are taken, default value is 0, 5, 10, 15, 20
phot0 = 0
phot1 = 5
phot2 = 10
phot3 = 15
phot4 = 20

#sets time for when the renaming process is going to happen, default is one hour after
ren0 = phot0+1
ren1 = phot1+1
ren2 = phot2+1
ren3 = phot3+1
ren4 = phot4+1

#used for testing the code
test1 = 15


#counts repeats of the while loop, can be commented out.
counter = 0

print('To escape loop, use Ctrl+C')
print()

while True is True:
    YMD = date.today()
    ymd = YMD.isoformat()
    hour = datetime.now().hour
    minute = datetime.now().minute

    #the lines below check if it is time for a photo, and uses the names photX and compares to the current hour, the os.path checks if a file is already created, to avoid duplicates
    if(((hour == phot0 or hour == phot1 or hour == phot2 or hour == phot3 or hour == phot4) is True and (os.path.exists('current.jpg') is False)) is True):
        #the call below calls for the camera module to take a picture, default name is current.jpg, commented out as the call does not work in a windows enviromnent
        #call (['raspistill -o current.jpg -q 100 -w 1920 -h 1080'], shell=True)
        print('image current.jpg taken')

    #the lines below check if it is time for renaming (default happens one hour after it takes the picture, as expressed by renX=photX+1
    if(((hour == ren0 or hour == ren1 or hour == ren2 or hour == ren3 or hour == ren4) is True and (os.path.exists('current.jpg') is True)) is True):
        os.rename('current.jpg', str(ymd)+'_'+str(int(hour)-1)+'.jpg')
        print('renamed the file current.jpg')

    #pauses the software, the value inside of () signals the amount of seconds
    time.sleep(2)
    
    #Use the below print() to signal that the software is moving forward during debug
    #print(str(hour))
    #print(str(minute))

    #Adds one to the counter, and shows the amount in the counter.s
    counter = counter+1
    print('Currently '+str(counter)+' returns done')
    print()
