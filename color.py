# NeoPixel set light to one color
# Author: James Stanfield


import time
from neopixel import *
import argparse
import sys

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-r','--red', action='store_true', help='Sets the color to red')
    parser.add_argument('-b','--blue', action='store_true', help='Sets the color to blue')
    parser.add_argument('-g','--green', action='store_true', help='Sets the color to green')
    parser.add_argument('-hex', type=lambda x: hex(int(x,0)), help='Enter hex code as argument')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        if args.red:
            print ('Setting color to red')
            while True:
               colorWipe(strip, Color(0, 175, 0))  # Red wipe

        elif args.blue:
           print ('Setting color to blue')
           while True:
               colorWipe(strip, Color(0, 0, 175))  # Blue wipe

        elif args.green:
           print ('Setting color to green')
           while True:
               colorWipe(strip, Color(175, 0, 0))  # Green wipe

        elif args.hex:
           print ('Setting color to %s' % args.hex)
           while True:
               colorWipe(strip, args.hex)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0))
