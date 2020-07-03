# Author: James Stanfield
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
#import cgi
#import cgitb
#cgitb.enable()

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
       strip.setPixelColor(i, color)
       strip.show()
       time.sleep(wait_ms/1000.0)

def fourthChase(strip, wait_ms=50):
    """Red White and Blue chase"""
    for i in range(3):
       for j in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+j, Color(0,255,0))
       for k in range(1, strip.numPixels(), 3):
          strip.setPixelColor(i+k, Color(127,127,127))
       for l in range(2, strip.numPixels(), 3):
          strip.setPixelColor(i+l, Color(0,0,255))
       strip.show()
       time.sleep(wait_ms/100.0)
       if (i == 0):
          strip.setPixelColor(i, Color(0,0,255))
          strip.show()
       if (i == 1):
          strip.setPixelColor(i-1, Color(127,127,127))
          strip.setPixelColor(i, Color(0,0,255))
          strip.show()

def oneLightRWB(strip, color, lightRange, wait_ms=50):
    """One light thru"""
    for i in range(lightRange):
       strip.setPixelColor(i, color)
       strip.show()
       strip.setPixelColor(i, Color(0,0,0))
       time.sleep(wait_ms/5000.0)
    strip.setPixelColor(lightRange-1, color)

def oneLightClear(strip, color, lightRange, wait_ms=50):
    """Clear the lights on close"""
    for i in reversed(range(lightRange)):
       strip.setPixelColor(i, color)
       strip.show()
       strip.setPixelColor(i, Color(0,0,0))
       time.sleep(wait_ms/5000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        print('Dads idea of Red White Blue')

        for i in range(0, strip.numPixels(), 3):
              oneLightRWB(strip, Color(0,255,0), strip.numPixels()-i)           #Red
              oneLightRWB(strip, Color(127,127,127), strip.numPixels()-i-1)     #White
              oneLightRWB(strip, Color(0,0,255), strip.numPixels()-i-2)         #Blue

        while True:
            fourthChase(strip)

    except KeyboardInterrupt:
        if args.clear:
           for i in reversed(range(0, strip.numPixels(), 3)):
              oneLightClear(strip, Color(0,0,255), strip.numPixels()-i-2)
              oneLightClear(strip, Color(127,127,127), strip.numPixels()-i-1)
              oneLightClear(strip, Color(0,255,0), strip.numPixels()-i)
           colorWipe(strip, Color(0,0,0))
