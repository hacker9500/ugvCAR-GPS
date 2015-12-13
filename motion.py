#!/usr/bin/python

"""The motion control Library"""

import time
import RPi.GPIO as GPIO
#import gps
import math

#from i2clibraries import i2c_hmc5883l

class MotionContol:
    """this class is going to control motor and will help to tackle obsacles"""
    fflag=None
    lflag=None
    rflag=None
    minDistance=40
    compassHeading=None
    hmc5883l=None

    def __init__(self):
        """this funtion intialises all the connections and do the required setup with the gpio configuration"""
        self.motoin1=23
        self.motorin2=22
        self.motoren=24
        self.trigger1=20
        self.trigger2=19
        self.trigger3=5
        self.echo1=21
        self.echo2=26
        self.echo3=6
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(self.motoin1,GPIO.OUT)
        GPIO.setup(self.motoin2,GPIO.OUT)
        self.p=GPIO.PWM(12,50)
        self.p.start(4)
        #session=gps.gps("localhost","2947")
        #session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        #self.hmc5883l=i2c_hmc5883l.i2c_hmc5883l(0)
        #self.hmc5883l.setContinuousMode()
        #self.hmc5883l.setDeclination(1,4)
"""
    def getCoordinates(self):
        this code returns current coordinate by list
        report=session.next()
        if report['class'] == 'TPV':
            if hasattr(report,'latitude')
                return [report.latitude,report.longitude]

    def getDirections(curr,destiny):
        this code aligns ugv towards the next destination with the help of compass
        self.compassHeading=self.hmc5883l.getHeading()
        self.compassHeading=self.compassHeading[0]+self.compassHeading[1]/60
        lat1=math.radians(curr[0])
        lat2=math.radians(destiny[0])
        diff=math.radians(destiny[1]-curr[1])
        x=math.sin(diff)*math.cos(lat2)
        y=math.cos(lat[1])*math.sin(lat[2])-(math.sin(lat1)*math.cos(lat2)*math.cos(diff))
        initial_bearing=math.atan2(x,y)
        initial_bearing=math.degrees(initial_bearing)
        heading=(initial_bearing+360)%360
        return (self.compassHeading-heading)

    def alignDirection(curr,destiny):
        this function takes the lat long coordinates and calculate the bearing
        heading=self.getDirections(curr,destiny)
        if heading>=(-180):
            if heading<=0:
                self.turnRigh()
        if heading<(-180):
            self.turnLeft()
        if heading>=0:
            if heading<180:
                self.turnLeft()
        if heading>=180:
            self.turnRigh()
        if heading==0:
            self.restore()
"""
    def UltrasonicDistance(self,trigger,echo):
        """this function calculates the distance calculated by the ultrasonic sensors"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.output(trigger, False)
        #time.sleep(1)
        GPIO.output(trigger, True)
        time.sleep(0.00001)
        GPIO.output(trigger, False)
        while GPIO.input(echo)==0:
            pulse_start=time.time()
        while GPIO.input(echo)==1:
            pulse_end=time.time()
        #claculating the pulse length
        pulse_duration=pulse_end-pulse_start
        #now calculating distance
        distance=pulse_duration*17150
        distance=round(distance,2)
        GPIO.cleanup()
        return distance

    def go(self):
        """move forward"""
        GPIO.output(self.motoren, True)
        GPIO.output(self.motoin1, True)
        GPIO.output(self.motoin2, False)
        self.fflag=1

    def restore(self):
        """restores servo to its mean position"""
        if self.lflag or self.rflag:
            self.p.ChangeDutyCycle(4)
            time.sleep(0.01)
            self.lflag=0
            self.rflag=0

    def turnLeft(self):
        """move servo to left"""
        if self.rflag:
            self.restore()
        if self.lflag:
            return
        self.p.ChangeDutyCycle(5.4)
        time.sleep(0.01)
        self.lflag=1

    def turnRight(self):
        """move servo to right"""
        if self.lflag:
            self.restore()
        if self.rflag:
            return
        self.p.ChangeDutyCycle(2.6)
        time.sleep(0.01)
        self.rflag=1

    def brake(self):
        """apply brakes"""
        GPIO.output(self.motoren, True)
        GPIO.output(self.motoin1, True)
        GPIO.output(self.motoin2, True)
        self.fflag=0

    def obstacle(self):
        """this function is to tackle the obstacles"""
        straight=self.UltrasonicDistance(self.trigger2,self.echo2)
        left=self.UltrasonicDistance(self.trigger1,self.echo1)
        right=self.UltrasonicDistance(self.trigger3,self.echo3)
        if(straight<=self.minDistance):
            if left<self.minDistance and right<self.minDistance:
                self.brake()
            elif left>right:
                self.brake()
                time.sleep(0.02)
                self.turnLeft()
                self.moveForward()
            elif right>left:
                self.brake()
                time.sleep(0.02)
                self.turnRight()
                self.moveForward()
        else:
            if not (lflag==0 and rflag==0):
                self.restore()
                self.moveForward()
                time.sleep(0.02)
        if(left>self.minDistance/2 and right<self.minDistance/2):
            self.brake()
            time.sleep(0.02)
            self.turnLeft()
            self.moveForward()
        elif(left<self.minDistance/2 and right>self.minDistance/2):
            self.brake()
            time.sleep(0.02)
            self.turnRight()
            self.moveForward()
        elif(left>self.minDistance/2 and right>self.minDistance/2)
            if not (lflag==0 and rflag==0):
                self.restore()
                self.moveForward()
                time.sleep(0.02)


    """def startMoving(self,destinationCoordinates):
        this function will start the movement by having a new destinationCoordinates which is a list with lat and long
        while self.getCoordinates() != destinationCoordinates:
            while(self.obstacle()):
                pass
            self.restore()
            self.alignDirection(self.getCoordinates(),destinationCoordinates)
        self.restore()
        self.brake()
        return 1"""

if __name__ == '__main__':
    ev=MotionContol()
    while True:
        self.obstacle()
        time.sleep(0.02)