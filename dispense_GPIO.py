import RPi.GPIO as GPIO
import urllib2
import time
import os
import sys

#change count on server to 0 

url = 'http://www.meldon.ca/app/count.html?count=0'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = { 'User-Agent' : user_agent }
req = urllib2.Request(url, None, headers)
response = urllib2.urlopen(req)
response.read(1)

def initiate():
        global servopin, BUTTON, treat_max, treat_day, servo
        #global BUTTON
        servopin = 21
        BUTTON = 20
        treat_max = 5  #maximum treats for the day
        treat_day = 0 #reset todays treat to 0
        #GPIO.setup(servopin,GPIO.OUT)
        #GPIO.setup(BUTTON,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #servo = GPIO.PWM(servopin,50)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servopin,GPIO.OUT)
        GPIO.setup(20,GPIO.OUT)
        servo = GPIO.PWM(servopin,50)
        servo.start(4)
        time.sleep(.5)
        servo.stop
        GPIO.cleanup()        
initiate

def check_web():
	global url, req, response
        while True:
               # if GPIO.input(BUTTON) == 0 :
                #GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=exit)
                #exit()
		url = 'http://meldon.ca/app/trigger.txt'
		req = urllib2.Request(url, None, headers)
		response = urllib2.urlopen(req)
                status = response.read(1)
                if status == "0":
                        # os.system('clear')
                        print "MONITORING SERVER..."
                elif status == "1":
                        print ">>REQUEST RECEIVED<<"
			url = 'http://meldon.ca/app/script.php?pi=reset'
			req = urllib2.Request(url, None, headers)
			response = urllib2.urlopen(req)
			status = response.read(1)
                        #urllib2.urlopen("http://meldon.ca/app/script.php?pi=reset").read(1)
                        give_treat()
                elif status == "6":
                	url = 'http://meldon.ca/app/script.php?pi=reset'
                        req = urllib2.Request(url, None, headers)
                        response = urllib2.urlopen(req)
                        status = response.read(1)
                        #urllib2.urlopen("http://meldon.ca/app/script.php?pi=reset").read(1)			
                        print ">>SHUTDOWN TRIGGER RECEIVED<<"
                        exit()
                time.sleep(5)
check_web

def give_treat():
        global treat_day, servopin	
        if treat_day < treat_max:
                #GPIO.setup(BUTTON,GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(servopin,GPIO.OUT)
                GPIO.setup(20,GPIO.OUT)
                servo = GPIO.PWM(servopin,50)
                treat_day +=1
                servo.start(3)
                time.sleep(.5)
                GPIO.output(20,1)
                servo.ChangeDutyCycle(13)
                time.sleep(.5)
                GPIO.output(20,0)
                servo.ChangeDutyCycle(3)
                time.sleep(.5)
                servo.stop
                GPIO.cleanup()
                print ""
                print "-----------------------------------------"
                print ">>>>>>>>>>>>>TREAT DISPENSED<<<<<<<<<<<<<"
                print "-----------------------------------------"
                print ""
                print "-----------------------------------------"
                print "-  THE DOG HAS HAD ", treat_day , " TREATS TODAY     -"
                print "-----------------------------------------"
                url = 'http://meldon.ca/app/count.html?count=' + str(treat_day)
                req = urllib2.Request(url, None, headers)
                response = urllib2.urlopen(req)
                status = response.read(1)
                #urllib2.urlopen("http://meldon.ca/app/count.html?count="  + str(treat_day)).read(1)
        else:
                print ""
                print "-----------------------------------------"
                print "-     MAX TREAT LIMIT FOR DAY REACHED   -"
                print "-----------------------------------------"
give_treat

def exit(ev=None):
        print ev
        url = 'http://meldon.ca/app/script.php?pi=reset'
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        status = response.read(1)
        #urllib2.urlopen("http://meldon.ca/app/script.php?pi=reset").read(1)
        sys.exit()

        
exit

initiate()
while True:
        try:
                #GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=exit)
                #what = raw_input("trigger>>")
                #if what == "click":
                       #give_treat()
               #elif what == "exit":
                        #exit()
                #elif what == "web":
                        check_web()
                #else:
                        #print "That trigger has not been programmed yet"
        except  KeyboardInterrupt:
                exit()
                GPIO.cleanup()
        
