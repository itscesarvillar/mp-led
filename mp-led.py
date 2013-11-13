import wiringpi2
import time
import os
import subprocess
import sys

io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
#mapping pins
leds = (8,7,0,3,12,14)
pushbottons = (9,2)

#setup pinout
for i in leds :
	io.pinMode(i,io.OUTPUT)
for i in pushbottons :
	io.pinMode(i, io.INPUT)
	io.pullUpDnControl(i, io.PUD_UP)

#global variables
volume = 50.0
step = 0.5
pause = True

# functions:
# when a button is pressed : control volume
# when both buttons are pressed: playPause
# adjustVolume - control the player by command line and
# control leds showing the volume level.
def controlVolume(buttonPressed, otherButton, step) :
	global volume
	while io.digitalRead(buttonPressed) == io.LOW :
		if io.digitalRead(otherButton) == io.LOW :
			break
		volume += step
		if volume > 100 :
			volume = 100.0
		if volume < 0 :
			volume = 0.0
		adjustVolume(volume)
		time.sleep(0.001)
	print 'volume ' + str(volume)

def playPause () :
	global pause
	if pause :
		#send  pause signal
		print 'pause'
		os.system('pkill -SIGSTOP mpg321')
		for i in range(2) :
			showLeds(0)
			time.sleep(0.2)
			threshold = 100.0/(len(leds)+1)
        		level = int(volume/threshold)
	        	showLeds(level)
			time.sleep(0.2)
	else :
		#send continue signal
		print 'resume'
		os.system('pkill -SIGCONT mpg321')
	while (io.digitalRead(pushbottons[0]) == io.LOW and
		io.digitalRead(pushbottons[1]) == io.LOW) :
		time.sleep(0.5)
	pause = not pause

def adjustVolume(volume) :
	os.system('amixer set PCM ' + str(volume) + '% >/dev/null')
	threshold = 100.0/(len(leds)+1) 
	level = int(volume/threshold)
	showLeds(level)

def showLeds(number) :
	for i in range(len(leds)) :
		if i < number :
			io.digitalWrite(leds[i], io.HIGH)
		else :
			io.digitalWrite(leds[i], io.LOW)

############################
# the program starts here! #
############################ 
#beginning animation
for i in range(3) :
	showLeds(i)
	time.sleep(0.1)
adjustVolume(volume)
#play the file given in argv
p = subprocess.Popen(['mpg321','/home/pi/music/' + sys.argv[1]])
while p.poll() == None: #wait until song is ended
	volumeUp  = io.digitalRead(pushbottons[0]) == io.LOW
	volumeDown = io.digitalRead(pushbottons[1]) == io.LOW
	if volumeUp :
		controlVolume(pushbottons[0], pushbottons[1], step)
	if volumeDown :
		controlVolume(pushbottons[1], pushbottons[0], -step)
	if volumeUp and volumeDown :
		playPause()
	time.sleep(0.3)
#ending animation
for i in range(len(leds))[::-1] :
	io.digitalWrite(leds[i], io.LOW)
	time.sleep(0.1)
print 'The song ' + sys.argv[1] + ' is ended'
