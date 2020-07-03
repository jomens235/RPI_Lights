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
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, start, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(start, strip.numPixels(), 2):
       strip.setPixelColor(i, color)
       strip.show()

def twoColors(strip, color, color2, wait_ms=50):
    """Set entire strip to two colors alternated"""
    for i in range(0, strip.numPixels(), 2):
       strip.setPixelColor(i, color)
    for j in range(1, strip.numPixels(), 2):
       strip.setPixelColor(j, color2)
       strip.show()
    time.sleep(wait_ms/10.0)

def oneColorFlash(strip, color, start, wait_ms=50, iterations=5):
    """Flash one of the two colors from above"""

    if (start == 0):
          colorWipe(strip, Color(0,0,0), start+1)
          colorWipe(strip, color, start)
          time.sleep(wait_ms/50.0)
          colorWipe(strip, Color(0,0,0), start)
          time.sleep(wait_ms/50.0)

    if (start == 1):
          colorWipe(strip, Color(0,0,0), start-1)
          colorWipe(strip, color, start)
          time.sleep(wait_ms/50.0)
          colorWipe(strip, Color(0,0,0), start)
          time.sleep(wait_ms/50.0)

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
        print('Kats Idea 1')
        while True:
            twoColors(strip, Color(127, 0, 0), Color(0,175,175))
            for i in range(5):
               oneColorFlash(strip, Color(127, 0, 0), 0)
               oneColorFlash(strip, Color(0,175,175), 1)

    except KeyboardInterrupt:
        if args.clear:
           colorWipe(strip, Color(0,0,0), 0)
           colorWipe(strip, Color(0,0,0), 1)
