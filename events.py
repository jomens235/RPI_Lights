import threading
from sequences import *
import time
import sys
from Queue import Queue

def setup_daemon_thread(runner, event, strip):
#Creates a daemon thread to twinkle screen whenever event is set. Returns event, threadhandle
    event = threading.Event()
    thread = threading.Thread(target=runner, args=(event,strip,))
    thread.daemon = True
    thread.start()
    return event, thread

def setup_spec_thread(runner, event, strip, args1, args2, args3):
    event = threading.Event()
    thread = threading.Thread(target=runner, args=(event, strip, args1, args2, args3,))
    thread.daemon = True
    thread.start()
    return event, thread

def twinkler(twinkleEvent, strip):
#Call twinkleTest whenever the given twinkleEvent is set and keeps calling until toggled
#Designed to be used in a separate thread.
    while True:
          twinkleEvent.wait()
          twinkleTest(strip, False, 20)
         #trandomLight(strip)

def randTwinkleRunner(randTwinkleEvent, strip):
    while True:
          randTwinkleEvent.wait()
          randTwinkle(strip)

def meteorRunner(meteorEvent, strip):
    while True:
          meteorEvent.wait()
          meteorRain(strip, 0x00, 0xff, 0xff, 10, 20, True)

def fireRunner(fireEvent, strip):
    while True:
          fireEvent.wait()
          Fire(strip, 55, 120)

def fourthFlashRunner(fourthEvent, strip):
    while True:
          fourthEvent.wait()
          fourthChase(strip)

def sparkleRunner(sparkleEvent, strip):
    while True:
          sparkleEvent.wait()
          sparkle(strip, 140, 120, 30)

def katIdea1Runner(katEvent, strip):
    while True:
          katEvent.wait()
          twoColors(strip, Color(127, 0, 0), Color(0, 175, 175))
          for i in range(5):
              oneColorFlash(strip, Color(127, 0, 0), 0)
              oneColorFlash(strip, Color(0, 175, 175), 1)

def eachRandomRunner(eachRandomEvent, strip):
    while True:
          eachRandomEvent.wait()
          eachRandom(strip)

def rainTheaterRunner(rainTheaterEvent, strip):
    while True:
          rainTheaterEvent.wait()
          theaterChaseRainbow(strip)

def oneLoopRunner(oneLoopEvent, strip):
    while True:
          oneLoopEvent.wait()
          oneLight(strip)
          oneLightBack(strip)

def sadKat1Runner(sadKatEvent, strip):
    while True:
          sadKatEvent.wait()
          sadKat1(strip)

def rainbowRunner(rainbowEvent, strip):
    while True:
          rainbowEvent.wait()
          rainbow(strip)

def cylonRunner1(cylonEvent, strip):
    while True:
          cylonEvent.wait()
          cylon(strip, 0xff, 0, 0, 4, 60, 0)

def cylonRunner2(cylonEvent, strip):
    while True:
          cylonEvent.wait()
          cylon(strip, 0xff, 0, 0, 4, 120, 61)

def cylonRunner3(cylonEvent, strip):
    while True:
          cylonEvent.wait()
          cylon(strip, 0xff, 0, 0, 4, 180, 121)

def cylonRunner4(cylonEvent, strip):
    while True:
          cylonEvent.wait()
          cylon(strip, 0xff, 0, 0, 4, 240, 181)

def cylonRunner5(cylonEvent, strip):
    while True:
          cylonEvent.wait()
          cylon(strip, 0xff, 0, 0, 4, 300, 241)

def cylonRunner6(cylonEvent, strip):
    while True:
          cylonEvent.wait()
          cylon(strip, 0xff, 0, 0, 4, 360, 301)

def runningLightsRunner(runningLightsEvent, strip):
    while True:
          runningLightsEvent.wait()
          runningLights(strip)

def RGBFlashRunner(RGBFlashEvent, strip):
    while True:
          RGBFlashEvent.wait()
          RGBFlash(strip)

def knockoffCylonRunner(knockoffCylonEvent, strip, green, red, blue):
    while True:
          knockoffCylonEvent.wait()
          knockoffCylon(strip, red, green, blue, 4, 60, 0)

def redWaveRunner(redWaveEvent, strip):
    while True:
          redWaveEvent.wait()
          redWave(strip)

def strobeRunner(strobeEvent, strip):
    while True:
          strobeEvent.wait()
          strobe(strip)

def pulseRunner(pulseEvent, strip):
    while True:
          pulseEvent.wait()
          pulse(strip)

def sineTwinkleRunner(sineEvent, strip):
    while True:
          sineEvent.wait()
          sineTwinkle(strip)
