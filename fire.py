# Meteor throughout strip
# Author: James Stanfield

import time
from neopixel import *
import argparse
import struct
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

#Cool down every cell a little
def Fire(strip, cooling, sparking, wait_ms=50):
    heat = [0] * LED_COUNT
    for i in range(LED_COUNT):
        cooldown = randint(0, ((cooling * 10)/LED_COUNT) + 2)
    if (cooldown > heat[i]):
        heat[i] = 0
    else:
        heat[i] = heat[i]-cooldown
    #Step 2: Heat from every cell drifts 'up' and diffuses a little
    for k in reversed(range(2, LED_COUNT - 1)):
        heat[k] = (heat[k-1] + heat[k-2] + heat[k-2])/3
    #Step 3: Randomly ignite new 'sparks' near the bottom
    if (randint(0, 255) < sparking):
        y = randint(0, 7)
        heat[y] = heat[y] + randint(160, 255)
    #Step 4: Convert heat to LED colors
    for j in range(LED_COUNT):
        setPixelHeatColor(strip, j, heat[j])
    strip.show()
    time.sleep(0.03)

def setPixelHeatColor(strip, pixel, temperature):
    t192 = round((temperature/255.0)*191)
    heatramp = int (t192) & 0x3F
    heatramp <<= 2

    #Figure out which third of the spectrum we're in
    if (t192 > 0x80):     #Hottest
        strip.setPixelColor(pixel, Color(255, 255, heatramp))
    elif (t192 > 0x40):   #Middle
        strip.setPixelColor(pixel, Color(heatramp, 255, 0))
    else:                 #Coolest
        strip.setPixelColor(pixel, Color(0, heatramp, 0))



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

        print ('Fire is burning!')

        while True:
             Fire(strip, 55, 120)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0))
