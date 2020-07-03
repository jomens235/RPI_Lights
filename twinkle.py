# Random twinkle lights throughout strip
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

def twinkleTest(strip, onlyOne, count, wait_ms=50):
    colorWipe(strip, Color(0,0,0))
    for i in range(count):
        strip.setPixelColor(randint(0,LED_COUNT), Color(170, 180, 30))
        strip.show()
        time.sleep(wait_ms/250.0)
        if (onlyOne):
           colorWipe(strip, Color(0,0,0))
    time.sleep(wait_ms/500.0)

class Twinkle():
    def fadeIn(self, strip, pixel, wait_ms=50):
        """Fade the light in"""
        for i in range(LED_BRIGHTNESS):
            strip.setPixelColor(pixel, Color(i/2, i, 0))
            strip.show()
  #          time.sleep(wait_ms/10000.0)

    def fadeOut(self, strip, pixel, wait_ms=50):
        for i in reversed(range(LED_BRIGHTNESS)):
            strip.setPixelColor(pixel, Color(i/2, i, 0))
            strip.show()
 #           time.sleep(wait_ms/10000.0)

    def randomLight(self, strip, wait_ms=50):
        """Attempt at turning on random lights throughout strip"""
#        for i in range(10):
        pixel = randint(0, LED_COUNT)
        self.fadeIn(strip, pixel)
#            time.sleep(wait_ms/5000.0)
        self.fadeOut(strip, pixel)


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

        print ('Lighting up random lights')
        #lightsOn = [Twinkle() for x in range(10)]
        light1 = Twinkle()

        while True:
          #  for i in range(10):
              # lightsOn.append(Twinkle())
           #    while lightsOn:
            #      lightsOn[i].randomLight(strip)
 #            for i in range(10):
#                light1.randomLight(strip)
             twinkleTest(strip, False, 10)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0))
