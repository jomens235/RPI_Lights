from OSC import OSCServer,OSCClient, OSCMessage
import sys
from time import sleep
import time
import types
import os
import RPi.GPIO as GPIO
from neopixel import *
from americanDad import *
from meteor import *
from fire import *
from fourthFlash import *
from oneLightThru import *
from oneLightThruLoop import *
from katIdea1 import *
from sadKat1 import *
from twinkle import *
from sparkle import *
from strandtest import *
from off import *
from random import seed
from random import randint
seed(1)


server = OSCServer( ("10.0.0.123", 8000) ) #This has to be the IP of the R-Pi on the network
client = OSCClient()

# LED Strip config:
LED_COUNT       = 60        # Num of LEDs in strip
LED_PIN         = 18        # GPIO pin connected to pixels
LED_FREQ_HZ     = 800000    # LED signal freq in herz
LED_DMA         = 10        # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = 200       # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False     # True to invert signal
LED_CHANNEL     = 0         # Set to '1' for GPIOs 13, 19, 41, 45, or 53


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

red = green = blue = 0

americanState = twinkleState = meteorState = fireState = 0
fourthState = sparkleState = katIdea1State = strandState = 0
oneLightState = oneLoopState = sadKat1State = 0

#def handle_timeout(self):
	#print ("Awaiting instruction...")
#This here is just to do something while the script receives no information....
#server.handle_timeout = types.MethodType(handle_timeout, server)

# FADERS
#################################################################################################################################################
def redFader(path, tags, args, source):
    global red, green, blue
    red = int(args[0]) #Value is the variable that will transform the input from the faders into whole numbers(easier to deal with); it will also get the 'y' value of the XP pads
    print "Red:", red
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(green, red, blue))
    strip.show()

def greenFader(path, tags, args, source):
    global red, green, blue
    green = int(args[0])
    print "Green: ", green
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(green, red, blue))
    strip.show()

def blueFader(path, tags, args, source):
    global red, green, blue
    blue = int(args[0])
    print "Blue: ", blue
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(green, red, blue))
    strip.show()

def brightFader(path, tags, args, source):
    value = int(args[0])
    print "Brightness: ", value
    for i in range(LED_COUNT):
        strip.setBrightness(value)
    strip.show()

# XY PADS
###############################################################################################################################################
def xypad(path, tags, args, source):
	 yy=int(args[0])
	 xx=int(args[1]) #Value 2 is used with XP pads, it will get the 'x' value
	 print "Value of Y:", yy,  "    Value of X:", xx


# BUTTONS
####################################################################################################################################################
def kill_switch(path, tags, args, source):
	state=int(args[0])
        turnOff(strip)
	print "Kill Switch:", state
	if state:
	   server.close() #THIS IS THE EMERGENCY KILL BUTTON!

def offBtn(path, tags, args, source):
       state=int(args[0])
       if state:
          turnOff(strip)

def americanDadBtn(path, tags, args, source):
       global americanState
       americanState=int(args[0])
       if americanState:
          turnOff(strip)
          for i in range(0, LED_COUNT, 3):
               oneLightRWB(strip, Color(0, 255, 0), strip.numPixels()-i)        #Red
               oneLightRWB(strip, Color(127, 127, 127), strip.numPixels()-i-1)  #White
               oneLightRWB(strip, Color(0, 0, 255), strip.numPixels()-i-2)      #Blue
               while americanState:
                     fourthChase(strip)
       if not americanState:
          turnOff(strip)

def twinkleBtn(path, tags, args, source):
       global twinkleState
       twinkleState=int(args[0])
       if twinkleState:
          turnOff(strip)
          while twinkleState:
               twinkleTest(strip, False, 10)
       if not twinkleState:
          turnOff(strip)

def meteorBtn(path, tags, args, source):
       global meteorState
       meteorState=int(args[0])
       if meteorState:
          turnOff(strip)
          while meteorState:
               meteorRain(strip, 0x00, 0xff, 0xff, 10, 20, True)
       if not meteorState:
          turnOff(strip)

def fireBtn(path, tags, args, source):
       global fireState
       fireState=int(args[0])
       if fireState:
          turnOff(strip)
          while fireState:
               Fire(strip, 55, 120)
       if not fireState:
          turnOff(strip)

def fourthFlashBtn(path, tags, args, source):
       global fourthState
       fourthState=int(args[0])
       if fourthState:
          turnOff(strip)
          while fourthState:
               fourthChase(strip)
       if not fourthState:
          turnOff(strip)

def sparkleBtn(path, tags, args, source):
       global sparkleState
       sparkleState=int(args[0])
       if sparkleState:
          turnOff(strip)
          while sparkleState:
               sparkle(strip, 140, 120, 30)
       if not sparkleState:
          turnOff(strip)

def katIdea1Btn(path, tags, args, source):
       global katIdea1State
       katIdea1State = int(args[0])
       if katIdea1State:
          turnOff(strip)
          while katIdea1State:
               twoColors(strip, Color(127, 0, 0), Color(0, 175, 175))
               for i in range(5):
                   oneColorFlash(strip, Color(127, 0, 0), 0)
                   oneColorFlash(strip, Color(0, 175, 175), 1)
       if not katIdea1State:
          turnOff(strip)

def strandTestBtn(path, tags, args, source):
       global strandState
       strandState = int(args[0])
       if strandState:
          turnOff(strip)
          while strandState:
               colorWipe(strip, Color(255, 0, 0))
               colorWipe(strip, Color(0, 255, 0))
               colorWipe(strip, Color(0, 0, 255))
               theaterChase(strip, Color(127, 127, 127))
               theaterChase(strip, Color(127, 0, 0))
               theaterChase(strip, Color(0, 0, 127))
               rainbow(strip)
               rainbowCycle(strip)
               theaterChaseRainbow(strip)
       if not strandState:
          turnOff(strip)

def oneLightThruBtn(path, tags, args, source):
        global oneLightState
        oneLightState = int(args[0])
        if oneLightState:
           turnOff(strip)
           while oneLightState:
                oneLight(strip, Color(255, 0, 0))
        if not oneLightState:
           turnOff(strip)

def oneLightLoopBtn(path, tags, args, source):
        global oneLoopState
        oneLoopState = int(args[0])
        if oneLoopState:
           turnOff(strip)
           while oneLoopState:
                oneLight(strip, Color(255, 0, 0))
                oneLightBack(strip, Color(255, 0, 0))
        if not oneLoopState:
           turnOff(strip)

def sadKat1Btn(path, tags, args, source):
        global sadKat1State
        sadKat1State = int(args[0])
        if sadKat1State:
           turnOff(strip)
           while sadKat1State:
                fade(strip)
        if not sadKat1State:
           turnOff(strip)

def autopilot(path, tags, args, source):
	state=int(args[0])
	print "Autopilot: ", state;


# ACCELEROMETER (will only work if you have the Accelerometer option on, in the TouchOSC app)
###################################################################################################################################################
def accel(path, tags, args, source):
	y=float(args[0])
	x=float(args[1])
	z=float(args[2])
	print "X:", x
	print "Y:", y
	print "Z:", z
	print " "
	time.sleep(3);


#These are all the add-ons that you can name in the TouchOSC layout designer (you can set the values and directories)
server.addMsgHandler("/main/brightness", brightFader)
server.addMsgHandler("/main/redCtl", redFader)
server.addMsgHandler("/main/greenCtl", greenFader)
server.addMsgHandler("/main/blueCtl", blueFader)
server.addMsgHandler("/programs/kill", kill_switch)
server.addMsgHandler("/programs/offBtn", offBtn)
server.addMsgHandler("/programs/americanDadBtn", americanDadBtn)
server.addMsgHandler("/programs/twinkleBtn", twinkleBtn)
server.addMsgHandler("/programs/meteorBtn", meteorBtn)
server.addMsgHandler("/programs/fireBtn", fireBtn)
server.addMsgHandler("/programs/fourthFlashBtn", fourthFlashBtn)
server.addMsgHandler("/programs/sparkleBtn", sparkleBtn)
server.addMsgHandler("/programs/katIdea1Btn", katIdea1Btn)
server.addMsgHandler("/programs/strandTestBtn", strandTestBtn)
server.addMsgHandler("/programs/oneLightThruBtn", oneLightThruBtn)
server.addMsgHandler("/programs/oneLightLoopBtn", oneLightLoopBtn)
server.addMsgHandler("/programs/sadKat1Btn", sadKat1Btn)
#server.addMsgHandler("/programs/TBD", TBD)

#server.addMsgHandler("/1/xypad", xypad)
#server.addMsgHandler("/1/toggle2", autopilot)
#server.addMsgHandler("accxyz", accel) #The Accelerometeer Values

#The way that the MSG Handlers work is by taking the values from set accessory, then it puts them into a function
#The function then takes the values and separates them according to their class (args, source, path, and tags)

while True:
	server.handle_request()

server.close()
#This will kill the server when the program ends
