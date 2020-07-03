# Random twinkle lights throughout strip
# Author: James Stanfield

import time
from neopixel import *
import argparse
from random import seed
from random import randint
seed(1)

import logging
import threading
import time

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

def fader(self, strip, pixel, wait_ms=50):
    """Fade the light in"""
    for i in range(LED_BRIGHTNESS):
        strip.setPixelColor(pixel, Color(i/2, i, 0))
        strip.show()
        time.sleep(wait_ms/100.0)
    """Fade the light out"""
    for i in reversed(range(LED_BRIGHTNESS)):
        strip.setPixelColor(pixel, Color(i/2, i, 0))
        strip.show()
        time.sleep(wait_ms/100.0)
    activeLights.pop(pixel)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    info = {"stop" : False}

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        colorWipe(strip, Color(0,0,0))

        activeLights = {}
        print ('Lighting up random lights')
        while True:
            print(activeLights)
            if len(activeLights) < 10:
                pixel = randint(0, LED_COUNT)
                print("pixel = " + str(pixel))
                if (len(activeLights) == 0) or (not activeLights.has_key[pixel]):
                    activeLights = { pixel : threading.Thread(target = fader, args = (info,strip,pixel)) }
                    activeLights[pixel].start()
            time.sleep(500.0)

    except KeyboardInterrupt:
        info["stop"] = True
        if args.clear:
            colorWipe(strip, Color(0,0,0))
