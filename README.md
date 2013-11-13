mp-led
======

mp3 player controlled by gpio. Raspberry pi
Academic assignment.

Requirements:

	- Raspbian or any other OS. Python.
	- Mpg321 mp3 player http://mpg321.sourceforge.net/
	- wiringPi2 https://projects.drogon.net/raspberry-pi/wiringpi/

Hardware:

	-Leds (indicator-level) use pins: 8 - 7 - 0 - 3 - 12 -14
	-Push-buttons use pins: 9 (volumeUp) 2 (volumeDown) 

Usage:

	sudo python mp-led.py <name_mp3_file>

	Where <name_mp3_file> has to be store in /home/pi/music
	Super user priviliges needed because of wiringPi2 to control GPIO

