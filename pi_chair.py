#!/usr/bin/env python

""" 
Uses Sunfounder Ultrasonic Rangefinder to estimate and track user''s weight over a period.
Uses code from the Sunfounder 
Sensor Kit example for that device.
This sample code tracks user''s weight over a week and draws a scatter plot in Google spreadsheet. 

"""

import RPi.GPIO as GPIO
import time
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import datetime


#Access to Google spreadsheet for storing data
json_key = json.load(open('clientid.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

#open the specific spreadsheet which collects data
wks = gc.open("chair").sheet1



#Uses ultrasonic rangefinder to caculate distance
Trig = 17
Echo = 18
Led = 27
DistanceForOneSecond = 200.0  # if we let it blink too slowly, it appears stopped
CHAIR_UP_POSITION = 66
CHAIR_DOWN_POSITION =62

def setup():
        GPIO.setmode(GPIO.BCM)  # BCM naming applies in this program
        GPIO.setup(Trig, GPIO.OUT)
        GPIO.setup(Echo, GPIO.IN)
        GPIO.setup(Led, GPIO.OUT)

def distance1():    # this function is from Sunfounder
        GPIO.output(Trig, 0)
        time.sleep(0.000002)  # magic from Sunfounder, presumably so the device can do its thing

        GPIO.output(Trig, 1)
        time.sleep(0.00001)   # magic from Sunfounder, presumably so the device can do its thing
        GPIO.output(Trig, 0)

        
        while GPIO.input(Echo) == 0:
                a = 0
        time1 = time.time()
        while GPIO.input(Echo) == 1:
                a = 1
        time2 = time.time()

        during = time2 - time1
        return during * 340 / 2 * 100

#average 3 readings to minimize variation        
def distance():
        sum =0
        for i in range(3):
                sum+= distance1()
        return sum/3   

#code to track chair position             
def loop():
        
        dis = distance()
        print "NOT SITTING", "distance above ground: " , dis, "cm"
        
        while dis > CHAIR_UP_POSITION :
                dis = distance()
                
        t1 = time.time()
        movement = False
        while dis > CHAIR_DOWN_POSITION:
                
                time.sleep(0.05)
                dis = distance()
                
                
                if dis < (CHAIR_UP_POSITION-CHAIR_DOWN_POSITION)/2:
                        movement = True
                print "GOING DOWN", "distance above ground:", dis, "cm"
        if movement:
                time_taken = time.time() - t1
                print "time_taken", time_taken
                day = datetime.datetime.today().weekday()
                prev = float(wks.cell(11+day, 3).value)
                num = float(wks.cell(11+day, 4).value)
                wks.update_cell(11+day, 3, (time_taken+prev)/(num+1))
                wks.update_cell(11+day, 4, (num+1))
                dis = distance()
                
                while dis < CHAIR_UP_POSITION:
                        dis = distance()
                        
                loop()        
        else:        
                loop()
                
def destroy():
        print "cleaning up"
        GPIO.cleanup()

if __name__ == "__main__":
        setup()
        try:
                print "calling loop"
                loop()
        except KeyboardInterrupt:
                destroy()
