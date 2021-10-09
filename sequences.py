from neopixel import *
import time
from random import seed
from random import randint
import math
import vars
seed(1)

# All of the NeoPixel functions to be used with TouchOSC

# Define functions which animate LEDs in various ways.
# Set all colors
def setAll(strip, color):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def turnOffPart(strip, downRange, upRange):
    for i in range(downRange, upRange):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

# Strand Test functions
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

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

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# SadKat1 Functions
def sadKat1(strip, wait_ms=20, iterations=1):
    for i in range(256*iterations):
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, bluePurpleWheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def bluePurpleWheel(pos):
    """Generate Blue and Purple colors across 0-255 positions."""
    if pos < 85:
        return Color(100-pos, 0, 255-pos*3)    #No blue  -- now no red
    elif pos < 170:
        pos -= 85
        return Color(0, 0, 255 - pos * 3)    #No red
    else:
        pos -= 170
        return Color(0, 100-pos, 255-pos*3)    #No green

# Twinkle function(s)
def twinkleTest(strip, onlyOne, count, wait_ms=50):
    turnOff(strip)
    for i in range(count):
        strip.setPixelColor(randint(0, strip.numPixels()), Color(170, 180, 30))
        strip.show()
        time.sleep(wait_ms/250.0)
        if (onlyOne):
           turnOff(strip)
    time.sleep(wait_ms/500.0)

def tfadeIn(strip, pixel, wait_ms=50):
    for i in range(210):
        strip.setPixelColor(pixel, Color(i/2, i, 0))
        strip.show()

def tfadeOut(strip, pixel, wait_ms=50):
    for i in reversed(range(210)):
        strip.setPixelColor(pixel, Color(i/2, i, 0))
        strip.show()

def trandomLight(strip, wait_ms=50):
    pixel = randint(0, strip.numPixels())
    tfadeIn(strip, pixel)
    tfadeOut(strip, pixel)

# Turn off function
def turnOff(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

# Fire functions
def Fire(strip, cooling, sparking, wait_ms=50):
    heat = [0] * strip.numPixels()
    for i in range(strip.numPixels()):
        cooldown = randint(0, ((cooling * 10)/strip.numPixels()) +2)
    if (cooldown > heat[i]):
       heat[i] = 0
    else:
       heat[i] = heat[i] - cooldown
    # Step 2: Heat from every cell drifts 'up' and diffuses a little
    for k in reversed(range(2, strip.numPixels() - 1)):
        heat[k] = (heat[k-1] + heat[k-2] + heat[k-2])/3
    # Step 3: Randomly ignite new 'sparks' near the bottom
    if (randint(0, 255) < sparking):
       y = randint(0,7)
       heat[y] = heat[y] + randint(160, 255)
    # Step 4: Convert heat to LED colors
    for j in range(strip.numPixels()):
        setPixelHeatColor(strip, j, heat[j])
    strip.show()
    time.sleep(0.03)

def setPixelHeatColor(strip, pixel, temperature):
    t192 = round((temperature/255.0)*191)
    heatramp = int(t192) & 0x3F
    heatramp <<= 2

    # Figure out which third of the spectrum we're in
    if (t192 > 0x80):   # Hottest
       strip.setPixelColor(pixel, Color(255, 255, heatramp))
    elif (t192 > 0x40): # Middle
       strip.setPixelColor(pixel, Color(heatramp, 255, 0))
    else:               # Coolest
       strip.setPixelColor(pixel, Color(0, heatramp, 0))

# Fourth Flash functions & americanDad
def fourthChase(strip, wait_ms=50):
    # RW&B Chase
    for i in range(3):
        for j in range(0, strip.numPixels(), 3):
            strip.setPixelColor(i+j, Color(0, 255, 0))
        for k in range(1, strip.numPixels(), 3):
            strip.setPixelColor(i+k, Color(127, 127, 127))
        for l in range(2, strip.numPixels(), 3):
            strip.setPixelColor(i+l, Color(0, 0, 255))
        strip.show()
        time.sleep(wait_ms/100.0)
        if (i == 0):
           strip.setPixelColor(i, Color(0, 0, 255))
           strip.show()
        if (i == 1):
           strip.setPixelColor(i-1, Color(127, 127, 127))
           strip.setPixelColor(i, Color(0, 0, 255))
           strip.show()

def oneLightRWB(strip, color, lightRange, wait_ms=50):
    for i in range(lightRange):
        strip.setPixelColor(i, color)
        strip.show()
        strip.setPixelColor(i, Color(0,0,0))
#        time.sleep(wait_ms/500000.0)
    strip.setPixelColor(lightRange-1, color)

def oneLightClear(strip, color, lightRange, wait_ms=50):
    for i in reversed(range(lightRange)):
        strip.setPixelColor(i, color)
        strip.show()
        strip.setPixelColor(i, Color(0,0,0))
 #       time.sleep(wait_ms/500000.0)

# Kat Idea 1 functions
def katColors(strip, color, start, wait_ms=50):
    for i in range(start, strip.numPixels(), 2):
        strip.setPixelColor(i, color)
    strip.show()

def twoColors(strip, color, color2, wait_ms=50):
    for i in range(0, strip.numPixels(), 2):
        strip.setPixelColor(i, color)
    for j in range(1, strip.numPixels(), 2):
        strip.setPixelColor(j, color2)
    strip.show()
    time.sleep(wait_ms/10.0)

def oneColorFlash(strip, color, start, wait_ms=50, iterations=5):
    if (start == 0):
       katColors(strip, Color(0,0,0), start+1)
       katColors(strip, color, start)
       time.sleep(wait_ms/50.0)
       katColors(strip, Color(0,0,0), start)
       time.sleep(wait_ms/50.0)
    if (start == 1):
       katColors(strip, Color(0,0,0), start-1)
       katColors(strip, color, start)
       time.sleep(wait_ms/50.0)
       katColors(strip, Color(0,0,0), start)
       time.sleep(wait_ms/50.0)

# One Light Through & Loop
def oneLight(strip, wait_ms=50):
    for j in range(0, strip.numPixels()):
        strip.setPixelColor(j, Color(vars.green, vars.red, vars.blue))
        strip.show()
        strip.setPixelColor(j, Color(0,0,0))
        time.sleep(wait_ms/1000.0)

def oneLightBack(strip, wait_ms=50):
    for k in reversed(range(0, strip.numPixels())):
        strip.setPixelColor(k, Color(vars.green, vars.red, vars.blue))
        strip.show()
        strip.setPixelColor(k, Color(0,0,0))
        time.sleep(wait_ms/1000.0)

# Meteor functions
def meteorRain(strip, green, red, blue, meteorSize, meteorTrailDecay, meteorRandomDecay, wait_ms=50):
    setAll(strip, Color(0,0,0))
    for i in range(strip.numPixels() + (strip.numPixels()/2)):
        # Fade brightness all LEDs one step
        for j in range(strip.numPixels()):
            if ((not meteorRandomDecay) or (randint(0,10) > 5)):
               fadeToBlack(strip, j, meteorTrailDecay)
        # Draw Meteor
        for j in range(meteorSize):
            if ((i-j < strip.numPixels()) and (i-j >= 0)):
               strip.setPixelColor(i-j, Color(green, red, blue))
        strip.show()
        time.sleep(wait_ms/1250.0)

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

# Sparkle function
def sparkle(strip, green, red, blue, wait_ms=50):
    pixel = randint(0, strip.numPixels())
    strip.setPixelColor(pixel, Color(green, red, blue))
    strip.show()
    time.sleep(wait_ms/500)
    strip.setPixelColor(pixel, Color(0,0,0))

# Cylon function
def cylon(strip, red, green, blue, eyeSize, upRange, downRange, speedDelay=50, returnDelay=50):
    for i in range(downRange, upRange-eyeSize-2):
        #turnOff(strip)
        turnOffPart(strip, downRange, upRange)

        strip.setPixelColor(i, Color(green/10, red/10, blue/10))
        for j in range(eyeSize+1):
            strip.setPixelColor(i+j, Color(green, red, blue))
        strip.setPixelColor(i+eyeSize+1, Color(green/10, red/10, blue/10))
        strip.show()
        time.sleep(speedDelay/10000.0)
    time.sleep(returnDelay/5000.0)
    for k in reversed(range(downRange, upRange-eyeSize-2)):
        #turnOff(strip)
        turnOffPart(strip, downRange, upRange)

        strip.setPixelColor(k, Color(green/10, red/10, blue/10))
        for m in range(eyeSize+1):
            strip.setPixelColor(k+m, Color(green, red, blue))
        strip.setPixelColor(k+eyeSize+1, Color(green/10, red/10, blue/10))
        strip.show()
        time.sleep(speedDelay/10000.0)
    time.sleep(returnDelay/5000.0)

# Running Lights Function
def runningLights(strip):
    position = 0
    for j in range(strip.numPixels() + 20):
        position += 1
        for i in range(strip.numPixels()):
            # Sine wave 3 offset waves make a rainbow
            strip.setPixelColor(i, Color(int(((math.sin(i+position) * 127 + 128)/255)*vars.green), int(((math.sin(i+position) * 127 + 128)/255)*vars.red), int(((math.sin(i+position) * 127 + 128)/255)*vars.blue)))
        strip.show()
        time.sleep(vars.delay/1000.0)

# Turns strip a random color
def randomColor(strip):
    setAll(strip, Color(randint(0, 255), randint(0, 255), randint(0, 255)))

# Flashes GRB color on strip
def RGBFlash(strip):
    for i in range(3):
        if i == 0:
           setAll(strip, Color(255, 0, 0))
           time.sleep(vars.delay/50.0)
        elif i == 1:
           setAll(strip, Color(0, 255, 0))
           time.sleep(vars.delay/50.0)
        else:
           setAll(strip, Color(0, 0, 255))
           time.sleep(vars.delay/50.0)

def knockoffCylon(strip, red, green, blue, eyeSize, upRange, downRange, speedDelay=50, returnDelay=50):
    for i in range(downRange, upRange-eyeSize-2):
        strip.setPixelColor(i, Color(green/10, red/10, blue/10))
        for j in range(eyeSize+1):
            strip.setPixelColor(i+j, Color(green, red, blue))
        strip.setPixelColor(i+eyeSize+1, Color(green/10, red/10, blue/10))
        strip.show()
        time.sleep(speedDelay/10000.0)
    time.sleep(returnDelay/5000.0)
    for k in reversed(range(downRange, upRange-eyeSize-2)):
        strip.setPixelColor(k, Color(green/10, red/10, blue/10))
        for m in range(eyeSize+1):
            strip.setPixelColor(k+m, Color(green, red, blue))
        strip.setPixelColor(k+eyeSize+1, Color(green/10, red/10, blue/10))
        strip.show()
        time.sleep(speedDelay/10000.0)
    time.sleep(returnDelay/5000.0)

def redWave(strip, wait_ms=20, iterations=1):
    for i in range(256*iterations):
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, redYellowWheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def redYellowWheel(pos):
    """Generate Red and Yellow colors across 0-255 positions."""
    if pos < 85:
        return Color(70-(pos-15), 255 - pos * 3, 0)    #Yellow
    elif pos < 170:
        pos -= 85
        return Color(0, 255 - pos * 3, 0)    #Red
    else:
        pos -= 170
        return Color((255-pos*3)/5, 255-pos*3, 0)    #Orange

def christmas1(strip):
    for i in range(0, strip.numPixels(), 20):
        j = i
        while j < (i+10):
            strip.setPixelColor(j, Color(200, 0, 0))
            j+=1
        while j >= (i+10) and j < (i+20):
            strip.setPixelColor(j, Color(0, 200, 0))
            j+=1
    strip.show()

def randTwinkle(strip):
    green = [255, 0, 0, 125, 210, 0, 0, 150, 220, 0, 0, 0]
    red = [0, 255, 0, 255, 250, 250, 150, 0, 0, 0, 0, 0]
    blue = [0, 0, 255, 0, 0, 150, 150, 200, 150, 0, 0, 0]
    rands = [0] * strip.numPixels()
    currentgreen = [0] * strip.numPixels()
    currentred = [0] * strip.numPixels()
    currentblue = [0] * strip.numPixels()
    for k in range(strip.numPixels()):
        rands[k] = randint(0,11)
        strip.setPixelColor(k, Color(green[rands[k]], red[rands[k]], blue[rands[k]]))
        currentgreen[k] = green[rands[k]]
        currentred[k] = red[rands[k]]
        currentblue[k] = blue[rands[k]]
    strip.show()
    for j in range(strip.numPixels()):
        for i in range(strip.numPixels()):
            if currentgreen[i] < green[rands[i]]:
               currentgreen[i] += 1
               strip.setPixelColor(i, Color(currentgreen[i], currentred[i], currentblue[i]))
            if currentred[i] < red[rands[i]]:
               currentred[i] += 1
               strip.setPixelColor(i, Color(currentgreen[i], currentred[i], currentblue[i]))
            if currentblue[i] < blue[rands[i]]:
               currentblue[i] += 1
               strip.setPixelColor(i, Color(currentgreen[i], currentred[i], currentblue[i]))
            if currentgreen[i] == green[rands[i]] and currentred[i] == red[rands[i]] and currentblue[i] == blue[rands[i]]:
               if green[rands[i]] != 0:
                  currentgreen[i] -= 1
                  strip.setPixelColor(i, Color(currentgreen[i], currentred[i], currentblue[i]))
               if red[rands[i]] != 0:
                  currentred[i] -= 1
                  strip.setPixelColor(i, Color(currentgreen[i], currentred[i], currentblue[i]))
               if blue[rands[i]] != 0:
                  currentblue[i] -= 1
                  strip.setPixelColor(i, Color(currentgreen[i], currentred[i], currentblue[i]))

        strip.show()

def eachRandom(strip):
    """Set each pixel in the strip to a rand color"""
    for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i, Color(randint(0,255), randint(0,255), randint(0,255)))
    strip.show()

# Strobe function
def strobe(strip):
    setAll(strip, Color(vars.green, vars.red, vars.blue))
    time.sleep(vars.delay/75.0)
    setAll(strip, Color(0,0,0))
    time.sleep(vars.delay/75.0)

def pulse(strip):
    for i in range(10, 255):
        strip.setBrightness(i)
        strip.show()
        time.sleep(vars.delay/5000.0)
    for j in reversed(range(10, 255)):
        strip.setBrightness(j)
        strip.show()
        time.sleep(vars.delay/5000.0)

def sineTwinkle(strip):
    green = [0] * strip.numPixels()
    red = [0] * strip.numPixels()
    blue = [0] * strip.numPixels()
    for j in range(strip.numPixels()):
        green[j] = randint(0,255)
        red[j] = randint(0,255)
        blue[j] = randint(0,255)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(int(((math.sin(i) * 127 + 128)/255)*green[i]), int(((math.sin(i) * 127 + 128)/255)*red[i]), int(((math.sin(i) * 127 + 128)/255)*blue[i])))
    strip.show()
    time.sleep(vars.delay/150.0)


#HAVE: StrandTest, SadKat1, FourthChase
#      Fire, Off, Twinkle, katIdea1, oneLightLoop, oneLightThru
#      rainbow, meteor, sparkle, americanDad
