# Meteor throughout strip
# Author: James Stanfield

import time
from neopixel import *
import argparse
from random import seed
from random import randint
seed(1)

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
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def meteorRain(strip, green, red, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, wait_ms=50):
    colorWipe(strip, Color(0,0,0))
    for i in range(LED_COUNT+LED_COUNT):
        #Fade brightness all LEDs one step
        for j in range(LED_COUNT):
            if ((not meteorRandomDecay) or (randint(0,10) > 5)):
               fadeToBlack(strip, j, meteorTrailDecay)
        #Draw Meteor
        for j in range(meteorSize):
            if ((i-j < LED_COUNT) and (i-j >= 0)):
               strip.setPixelColor(i-j, Color(green, red, blue))
        strip.show()
        time.sleep(wait_ms/1500.0)

def fadeToBlack(strip, ledNo, fadeValue):
    oldColor = strip.getPixelColor(ledNo)
    r = (oldColor & 0x00ff0000) >> 16
    g = (oldColor & 0x0000ff00) >> 8
    b = (oldColor & 0x000000ff)
    if (r <= 10):
       r-(r*fadeValue/256)
    else:
       r = 0
    if (g <= 10):
       g-(g*fadeValue/256)
    else:
       g = 0
    if (b <= 10):
       b-(b*fadeValue/256)
    else:
       b = 0
    strip.setPixelColor(ledNo, Color(g,r,b))


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

        print ('Look out, a meteor is coming!')

        while True:
             meteorRain(strip, 0x00, 0xff, 0xff, 10, 20, True)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0))
