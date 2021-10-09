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
import vars
from events import *
from random import seed
from random import randint
seed(1)


server = OSCServer( ("10.0.0.123", 8000) ) #This has to be the IP of the R-Pi on the network
client = OSCClient()

# LED Strip config:
LED_COUNT       = 360        # Num of LEDs in strip
LED_PIN         = 18        # GPIO pin connected to pixels
LED_FREQ_HZ     = 800000    # LED signal freq in herz
LED_DMA         = 10        # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = 200       # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False     # True to invert signal
LED_CHANNEL     = 0         # Set to '1' for GPIOs 13, 19, 41, 45, or 53


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

vars.init()

stringLightsBool = False

twinkleEvent = twinkleThread = None
randTwinkleEvent = randTwinkleThread = None
meteorEvent = meteorThread = None
fireEvent = fireThread = None
fourthEvent = fourthThread = None
sparkleEvent = sparkleThread = None
katIdea1Event = katIdea1Thread = None
eachRandomEvent = eachRandomThread = None
rainTheaterEvent = rainTheaterThread = None
oneLoopEvent = oneLoopThread = None
sadKat1Event = sadKat1Thread = None
rainbowEvent = rainbowThread = None
cylonEvent = cylonThread = None
cylonEvent2 = cylonThread2 = None
cylonEvent3 = cylonThread3 = None
cylonEvent4 = cylonThread4 = None
cylonEvent5 = cylonThread5 = None
cylonEvent6 = cylonThread6 = None
runningLightsEvent = runningLightsThread = None
RGBFlashEvent = RGBFlashThread = None
knockoffCylonEvent = knockoffCylonThread = None
redWaveEvent = redWaveThread = None
strobeEvent = strobeThread = None
pulseEvent = pulseThread = None
sineEvent = sineThread = None

def handle_timeout(self):
	print ("Awaiting instruction...")
#This here is just to do something while the script receives no information....
#server.handle_timeout = types.MethodType(handle_timeout, server)


# FADERS
#################################################################################################################################################
def redFader(path, tags, args, source):
    global stringLightsBool
    red = int(args[0]) #Value is the variable that will transform the input from the faders into whole numbers(easier to deal with); it will also get the 'y' value of the XP pads
    print "Red:", red
    vars.red = red
    if stringLightsBool:
       for j in range(0, LED_COUNT, 8):
           strip.setPixelColor(j, Color(vars.green, vars.red, vars.blue))
       strip.show()
    else:
       for i in range(LED_COUNT):
           strip.setPixelColor(i, Color(vars.green, vars.red, vars.blue))
       strip.show()

def greenFader(path, tags, args, source):
    global stringLightsBool
    green = int(args[0])
    print "Green: ", green
    vars.green = green
    if stringLightsBool:
       for j in range(0, LED_COUNT, 8):
           strip.setPixelColor(j, Color(vars.green, vars.red, vars.blue))
       strip.show()
    else:
       for i in range(LED_COUNT):
           strip.setPixelColor(i, Color(vars.green, vars.red, vars.blue))
       strip.show()

def blueFader(path, tags, args, source):
    global stringLightsBool
    blue = int(args[0])
    print "Blue: ", blue
    vars.blue = blue
    if stringLightsBool:
       for j in range(0, LED_COUNT, 8):
           strip.setPixelColor(j, Color(vars.green, vars.red, vars.blue))
       strip.show()
    else:
       for i in range(LED_COUNT):
           strip.setPixelColor(i, Color(vars.green, vars.red, vars.blue))
       strip.show()

def brightFader(path, tags, args, source):
    value = int(args[0])
    print "Brightness: ", value
    for i in range(LED_COUNT):
        strip.setBrightness(value)
    strip.show()

def delayFader(path, tags, args, source):
    value = int(args[0])
    print "Delay value: ", value
    vars.delay = value

def intensityFader(path, tags, args, source):
    value = int(args[0])
    print "Intensity value: ", value
    vars.intensity = value


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

def strobeBtn(path, tags, args, source):
       global strobeThread, strobeEvent
       state=int(args[0])
       if strobeEvent is None:
          strobeEvent, strobeThread = setup_daemon_thread(strobeRunner, strobeEvent, strip)
       if strobeEvent.is_set():
          strobeEvent.clear()
       else:
          strobeEvent.set()

def pulseBtn(path, tags, args, source):
       global pulseThread, pulseEvent
       state=int(args[0])
       if pulseEvent is None:
          pulseEvent, pulseThread = setup_daemon_thread(pulseRunner, pulseEvent, strip)
       if pulseEvent.is_set():
          pulseEvent.clear()
       else:
          pulseEvent.set()

def randTwinkleBtn(path, tags, args, source):
       global randTwinkleEvent, randTwinkleThread
       randTwinkleState=int(args[0])
       if randTwinkleEvent is None:
          randTwinkleEvent, randTwinkleThread = setup_daemon_thread(randTwinkleRunner, randTwinkleEvent, strip)
       if randTwinkleEvent.is_set():
          randTwinkleEvent.clear()
       else:
          randTwinkleEvent.set()

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

def eachRandomBtn(path, tags, args, source):
       eachRandomState = int(args[0])
       if eachRandomState:
           eachRandom(strip)
       else:
           setAll(Color(gcolor.red, gcolor.green, gcolor.blue))

def rainbowTheaterBtn(path, tags, args, source):
        global rainTheaterEvent, rainTheaterThread
        rainTheaterState = int(args[0])
        if rainTheaterEvent is None:
           rainTheaterEvent, rainTheaterThread = setup_daemon_thread(rainTheaterRunner, rainTheaterEvent, strip)
        if rainTheaterEvent.is_set():
           rainTheaterEvent.clear()
        else:
           rainTheaterEvent.set()

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
        global cylonEvent, cylonThread, cylonEvent2, cylonThread2, cylonEvent3, cylonThread3, cylonEvent4, cylonThread4, cylonEvent5, cylonThread5, cylonEvent6, cylonThread6
        cylonState = int(args[0])
        if cylonEvent is None:
           cylonEvent, cylonThread = setup_daemon_thread(cylonRunner1, cylonEvent, strip)
#           cylonEvent2, cylonThread2 = setup_daemon_thread(cylonRunner2, cylonEvent2, strip)
#           cylonEvent3, cylonThread3 = setup_daemon_thread(cylonRunner3, cylonEvent3, strip)
#           cylonEvent4, cylonThread4 = setup_daemon_thread(cylonRunner4, cylonEvent4, strip)
#           cylonEvent5, cylonThread5 = setup_daemon_thread(cylonRunner5, cylonEvent5, strip)
#           cylonEvent6, cylonThread6 = setup_daemon_thread(cylonRunner6, cylonEvent6, strip)
        if cylonEvent.is_set():
           cylonEvent.clear()
#           cylonEvent2.clear()
#           cylonEvent3.clear()
#           cylonEvent4.clear()
#           cylonEvent5.clear()
#           cylonEvent6.clear()
        else:
           cylonEvent.set()
#           cylonEvent2.set()
#           cylonEvent3.set()
#           cylonEvent4.set()
#           cylonEvent5.set()
#           cylonEvent6.set()

def runningLightsBtn(path, tags, args, source):
       global runningLightsEvent, runningLightsThread
       runningState = int(args[0])
       if runningLightsEvent is None:
          runningLightsEvent, runningLightsThread = setup_daemon_thread(runningLightsRunner, runningLightsEvent, strip)
       if runningLightsEvent.is_set():
          runningLightsEvent.clear()
       else:
          runningLightsEvent.set()

def randColorBtn(path, tags, args, source):
       randState = int(args[0])
       randomColor(strip)

def RGBFlashBtn(path, tags, args, source):
       global RGBFlashEvent, RGBFlashThread
       rgbState = int(args[0])
       if RGBFlashEvent is None:
          RGBFlashEvent, RGBFlashThread = setup_daemon_thread(RGBFlashRunner, RGBFlashEvent, strip)
       if RGBFlashEvent.is_set():
          RGBFlashEvent.clear()
       else:
          RGBFlashEvent.set()

def knockoffCylonBtn(path, tags, args, source):
       global knockoffCylonEvent, knockoffCylonThread
       knockoffState = int(args[0])
       if knockoffCylonEvent is None:
          knockoffCylonEvent, knockoffCylonThread = setup_spec_thread(knockoffCylonRunner, knockoffCylonEvent, strip, vars.green, vars.red, vars.blue)
       if knockoffCylonEvent.is_set():
          knockoffCylonEvent.clear()
       else:
          knockoffCylonEvent.set()

def redWaveBtn(path, tags, args, source):
       global redWaveEvent, redWaveThread
       redWaveState = int(args[0])
       if redWaveEvent is None:
          redWaveEvent, redWaveThread = setup_daemon_thread(redWaveRunner, redWaveEvent, strip)
       if redWaveEvent.is_set():
          redWaveEvent.clear()
       else:
          redWaveEvent.set()

def stringLightsBtn(path, tags, args, source):
       global stringLightsBool
       stringLightState = int(args[0])
       if stringLightState:
          stringLightsBool = True
          turnOff(strip)
          for i in range(0, LED_COUNT, 8):
              strip.setPixelColor(i, Color(vars.green, vars.red, vars.blue))
          strip.show()
       else:
          stringLightsBool = False
          for j in range(LED_COUNT):
              strip.setPixelColor(j, Color(vars.green, vars.red, vars.blue))
          strip.show()

def christmasBtn(path, tags, args, source):
    christmasState = int(args[0])
    if christmasState:
       christmas1(strip)
    else:
       setAll(strip, Color(0,0,0))

def sineTwinkleBtn(path, tags, args, source):
    global sineEvent, sineThread
    sineState = int(args[0])
    if sineEvent is None:
       sineEvent, sineThread = setup_daemon_thread(sineTwinkleRunner, sineEvent, strip)
    if sineEvent.is_set():
       sineEvent.clear()
    else:
       sineEvent.set()

def autopilot(path, tags, args, source):
	state=int(args[0])
	print "Autopilot: ", state;


# ACCELEROMETER (will only work if you have the Accelerometer option on in the TouchOSC app)
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
server.addMsgHandler("/main/delayFader", delayFader)
server.addMsgHandler("/main/intensityFader", intensityFader)
server.addMsgHandler("/programs/kill", kill_switch)
server.addMsgHandler("/programs/offBtn", offBtn)
server.addMsgHandler("/programs/randTwinkleBtn", randTwinkleBtn) #Switched to random twinkle colors
server.addMsgHandler("/programs/twinkleBtn", twinkleBtn)
server.addMsgHandler("/programs/meteorBtn", meteorBtn)
server.addMsgHandler("/programs/fireBtn", fireBtn)
server.addMsgHandler("/programs/fourthFlashBtn", fourthFlashBtn)
server.addMsgHandler("/programs/sparkleBtn", sparkleBtn)
server.addMsgHandler("/programs/katIdea1Btn", katIdea1Btn)
server.addMsgHandler("/programs/eachRandomBtn", eachRandomBtn) # Switched from strand test to eachRandom
server.addMsgHandler("/programs/rainbowTheaterBtn", rainbowTheaterBtn) # Switched to rainbow theater cycle
server.addMsgHandler("/programs/oneLightLoopBtn", oneLightLoopBtn)
server.addMsgHandler("/programs/sadKat1Btn", sadKat1Btn)
server.addMsgHandler("/programs/rainbowBtn", rainbowBtn)
server.addMsgHandler("/programs/cylonBtn", cylonBtn)
server.addMsgHandler("/programs/runningLightsBtn", runningLightsBtn)
server.addMsgHandler("/programs/randColorBtn", randColorBtn)
server.addMsgHandler("/programs/RGBFlashBtn", RGBFlashBtn)
server.addMsgHandler("/programs/knockoffCylonBtn", knockoffCylonBtn)
server.addMsgHandler("/programs/redWaveBtn", redWaveBtn)
server.addMsgHandler("/programs/stringLightsBtn", stringLightsBtn)
server.addMsgHandler("/programs/christmasBtn", christmasBtn)
server.addMsgHandler("/programs/pulseBtn", pulseBtn)
server.addMsgHandler("/programs/strobeBtn", strobeBtn)
server.addMsgHandler("/programs/sineTwinkleBtn", sineTwinkleBtn)

#server.addMsgHandler("/1/xypad", xypad)
#server.addMsgHandler("/1/toggle2", autopilot)
#server.addMsgHandler("accxyz", accel) #The Accelerometeer Values

#The way that the MSG Handlers work is by taking the values from set accessory, then it puts them into a function
#The function then takes the values and separates them according to their class (args, source, path, and tags)

while True:
	server.handle_request()

server.close()
#This will kill the server when the program ends
