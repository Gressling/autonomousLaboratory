#!/usr/bin/python

import datetime
import time
import sys, os
import string

quality = 100
width = 320 #640
height = 200  #480
saturation = -100 #50
contrast = 70
brightness = 50
showTimeInMillis = 250
pauseTimeInMillis = 2000
#
objekt= str(sys.argv[1]).strip()
# Object will be saved in dir:
pathToSave=sys.path[0] + "/training/" 
#
def pic():
	command = "raspistill -vf -q " + str(quality) \
		+ " -w " + str(width) \
		+ " -h " + str(height) \
		+ " -sa " + str(saturation) \
		+ " -co " + str(contrast) \
		+ " -br " + str(brightness) \
		+ " -t " + str(showTimeInMillis) \
		+ " -o " + pathToSave+ str(objekt)+"-"+datetime.datetime.now().strftime("%M%S%f") \
                + ".jpg"
	print 'command : -> ', command
	os.system(command)
def main():
   while True:
      try:
	pic()
	sleeptime = pauseTimeInMillis/1000.0
	print("sleep: " + str(sleeptime) + "s")
	time.sleep(sleeptime)
      except KeyboardInterrupt:
        exit()

if __name__=='__main__':
     main()

