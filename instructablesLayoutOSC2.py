from OSC import OSCServer,OSCClient, OSCMessage
import sys
from time import sleep
import time
import types
import threading
import os
import RPi.GPIO as GPIO
from neopixel import *
from sequences import *
from events import *
from random import seed
from random import randint
seed(1)


server = OSCServer( ("10.0.0.123", 8000) ) #This has to be the IP of the R-Pi on the network
client = OSCClient()

# LED Strip config:
LED_COUNT       = 300        # Num of LEDs in strip
LED_PIN         = 18        # GPIO pin connected to pixels
LED_FREQ_HZ     = 800000    # LED signal freq in herz
LED_DMA         = 10        # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = 200       # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False     # True to invert signal
LED_CHANNEL     = 0         # Set to '1' for GPIOs 13, 19, 41, 45, or 53


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

red = green = blue = 0

twinkleEvent = twinkleThread = None
americanDadEvent = americanDadThread = None
meteorEvent = meteorThread = None
fireEvent = fireThread = None
fourthEvent = fourthThread = None
sparkleEvent = sparkleThread = None
katIdea1Event = katIdea1Thread = None
strandEvent = strandThread = None
oneLightEvent = oneLightThread = None
oneLoopEvent = oneLoopThread = None
sadKat1Event = sadKat1Thread = None
rainbowEvent = rainbowThread = None
cylonEvent = cylonThread = None
runningLightsEvent = runningLightsThread = None

#def handle_timeout(self):
	#print ("Awaiting instruction...")
#This here is just to do something while the script receives no information....
#server.handle_timeout = types.MethodType(handle_timeout, server)

def pulse(delay):
    if delay > 0:
       for i in range(10, 220):
           strip.setBrightness(i)
           strip.show()
           time.sleep(1.0/delay)
       for j in reversed(range(10, 220)):
           strip.setBrightness(j)
           strip.show()
           time.sleep(1.0/delay)

def strobe(delay):
    global red, green, blue
    while delay > 0:
          setAll(Color(green, red, blue))
          time.sleep(1.0/delay)
          setAll(Color(0,0,0))
          time.sleep(1.0/delay)


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

def strobeFader(path, tags, args, source):
    global red, green, blue
    value = int(args[0])
    print "Strobe value: ", value
    strobe(value)

def pulseFader(path, tags, args, source):
    global red, green, blue
    value = int(args[0])
    print "Pulse value: ", value
    pulse(value)


# XY PADS
###############################################################################################################################################
def xypad(path, tags, args, source):
	 yy=int(args[0])
	 xx=int(args[1]) #Value 2 is used with XP pads, it will get the 'x' value
	 print "Value of Y:", yy,  "    Value of X:", xx


# BUTTONS
####################################################################################################################################################
threads = list()

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
       global americanDadEvent, americanDadThread
       americanState=int(args[0])
       if americanDadEvent is None:
          americanDadEvent, americanDadThread = setup_daemon_thread(americanDadRunner, americanDadEvent, strip)
       if americanDadEvent.is_set():
          americanDadEvent.clear()
       else:
          americanDadEvent.set()

def twinkleBtn(path, tags, args, source):
       global twinkleEvent, twinkleThread
       twinkleState = int(args[0])
       if twinkleEvent is None:
          #start daemon thread on first use
          twinkleEvent, twinkleThread = setup_daemon_thread(twinkler, twinkleEvent, strip)
       if twinkleEvent.is_set():
          twinkleEvent.clear()
       else:
          twinkleEvent.set()

def meteorBtn(path, tags, args, source):
       global meteorEvent, meteorThread
       meteorState=int(args[0])
       if meteorEvent is None:
          meteorEvent, meteorThread = setup_daemon_thread(meteorRunner, meteorEvent, strip)
       if meteorEvent.is_set():
          meteorEvent.clear()
       else:
          meteorEvent.set()

def fireBtn(path, tags, args, source):
       global fireEvent, fireThread
       fireState=int(args[0])
       if fireEvent is None:
          fireEvent, fireThread = setup_daemon_thread(fireRunner, fireEvent, strip)
       if fireEvent.is_set():
          fireEvent.clear()
       else:
          fireEvent.set()

def fourthFlashBtn(path, tags, args, source):
       global fourthEvent, fourthThread
       fourthState=int(args[0])
       if fourthEvent is None:
          fourthEvent, fourthThread = setup_daemon_thread(fourthFlashRunner, fourthEvent, strip)
       if fourthEvent.is_set():
          fourthEvent.clear()
       else:
          fourthEvent.set()

def sparkleBtn(path, tags, args, source):
       global sparkleEvent, sparkleThread
       sparkleState=int(args[0])
       if sparkleEvent is None:
          sparkleEvent, sparkleThread = setup_daemon_thread(sparkleRunner, sparkleEvent, strip)
       if sparkleEvent.is_set():
          sparkleEvent.clear()
       else:
          sparkleEvent.set()

def katIdea1Btn(path, tags, args, source):
       global katIdea1Event, katIdea1Thread
       katIdea1State = int(args[0])
       if katIdea1Event is None:
          katIdea1Event, katIdea1Thread = setup_daemon_thread(katIdea1Runner, katIdea1Event, strip)
       if katIdea1Event.is_set():
          katIdea1Event.clear()
       else:
          katIdea1Event.set()

def strandTestBtn(path, tags, args, source):
       global strandEvent, strandThread
       strandState = int(args[0])
       if strandEvent is None:
          strandEvent, strandThread = setup_daemon_thread(strandTestRunner, strandEvent, strip)
       if strandEvent.is_set():
          strandEvent.clear()
       else:
          strandEvent.set()

def oneLightThruBtn(path, tags, args, source):
        global oneLightEvent, oneLightThread
        oneLightState = int(args[0])
        if oneLightEvent is None:
           oneLightEvent, oneLightThread = setup_daemon_thread(oneLightRunner, oneLightEvent, strip)
        if oneLightEvent.is_set():
           oneLightEvent.clear()
        else:
           oneLightEvent.set()

def oneLightLoopBtn(path, tags, args, source):
        global oneLoopEvent, oneLoopThread
        oneLoopState = int(args[0])
        if oneLoopEvent is None:
           oneLoopEvent, oneLoopThread = setup_daemon_thread(oneLoopRunner, oneLoopEvent, strip)
        if oneLoopEvent.is_set():
           oneLoopEvent.clear()
        else:
           oneLoopEvent.set()

def sadKat1Btn(path, tags, args, source):
        global sadKat1Event, sadKat1Thread
        sadKat1State = int(args[0])
        if sadKat1Event is None:
           sadKat1Event, sadKat1Thread = setup_daemon_thread(sadKat1Runner, sadKat1Event, strip)
        if sadKat1Event.is_set():
           sadKat1Event.clear()
        else:
           sadKat1Event.set()

def rainbowBtn(path, tags, args, source):
        global rainbowEvent, rainbowThread
        rainbowState = int(args[0])
        if rainbowEvent is None:
           rainbowEvent, rainbowThread = setup_daemon_thread(rainbowRunner, rainbowEvent, strip)
        if rainbowEvent.is_set():
           rainbowEvent.clear()
        else:
           rainbowEvent.set()

def cylonBtn(path, tags, args, source):
        global cylonEvent, cylonThread
        cylonState = int(args[0])
        if cylonEvent is None:
           cylonEvent, cylonThread = setup_daemon_thread(cylonRunner, cylonEvent, strip)
        if cylonEvent.is_set():
           cylonEvent.clear()
        else:
           cylonEvent.set()

def runningLightsBtn(path, tags, args, source):
       global runningLightsEvent, runningLightsThread
       runningState = int(args[0])
       if runningLightsEvent is None:
          runningLightsEvent, runningLightsThread = setup_daemon_thread(runningLightsRunner, runningLightsEvent, strip)
       if runningLightsEvent.is_set():
          runningLightsEvent.clear()
       else:
          runningLightsEvent.set()

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
server.addMsgHandler("/main/strobeFader", strobeFader)
server.addMsgHandler("/main/pulseFader", pulseFader)
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
server.addMsgHandler("/programs/rainbowBtn", rainbowBtn)
server.addMsgHandler("/programs/cylonBtn", cylonBtn)
server.addMsgHandler("/programs/runningLightsBtn", runningLightsBtn)
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
