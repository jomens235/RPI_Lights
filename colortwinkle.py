# Author: James Stanfield
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
import math
from random import randint

# LED strip configuration:
LED_COUNT      = 360      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 250     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def colorTwinkles(strip):
    """Attempt at recreating ColorTwinkles from WLED/FastLED"""
    green = [0] * strip.numPixels()
    red = [0] * strip.numPixels()
    blue = [0] * strip.numPixels()
    for j in range(strip.numPixels()):
        green[j] = randint(0,255)
        red[j] = randint(0,255)
        blue[j] = randint(0,255)
    for k in range(strip.numPixels()):
        for i in range(0, strip.numPixels(), 3):
            strip.setPixelColor(i, Color(int(((math.sin(k+randint(0,strip.numPixels())) * 127 + 128)/255)*green[i]), int(((math.sin(k+randint(0,strip.numPixels())) * 127 + 128)/255)*red[i]), int(((math.sin(k+randint(0,strip.numPixels())) * 127 + 128)/255)*blue[i])))
        strip.show()
        #time.sleep(1)

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

        while True:
	    colorTwinkles(strip) #Call Red White & Blue

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
