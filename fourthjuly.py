# Author: James Stanfield
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
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
        time.sleep(wait_ms/1000.0)

def redWhiteBlue(strip, wait_ms=50):
    """Set certain num of pixels to a color"""
    for i in range(strip.numPixels()):
        if (i < 10):
            strip.setPixelColor(i,0x00ff00)
            strip.show()
        if (i >= 10 and i < 20):
            strip.setPixelColor(i,0xffffff)
            strip.show()
        if (i >= 20 and i < 30):
            strip.setPixelColor(i,0x0000ff)
            strip.show()
        if (i >= 30 and i < 40):
           # strip.setPixelColor(i,0x00ff00)
            strip.setPixelColor(i,Color(0,255,0))
            strip.show()
        if (i >= 40 and i < 50):
            #strip.setPixelColor(i,0xffffff)
            strip.setPixelColor(i,Color(127,127,127))
            strip.show()
        if (i >= 50 and i <= 60):
            #strip.setPixelColor(i,0x0000ff)
            strip.setPixelColor(i,Color(0,0,255))
            strip.show()

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

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
        print('God Bless The USA')
    try:

        while True:

	    redWhiteBlue(strip) #Call Red White & Blue
            #colorWipe(strip, Color(255, 0, 0))  # Red wipe
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255))  # Green wipe
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
