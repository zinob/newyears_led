#!/usr/bin/python3

import tqdm
import time
from rpi_ws281x import PixelStrip, Color, ws

from math import ceil, modf
import time
import datetime
import random

midnight = datetime.time(23,59,58,50)

#MAX_TIME=3600 #How long before midnight to start filling the LED-strip (redefined below to be one led per minute)
IDLE_COLOR=Color(0,1,0,0)
SHINE_COLOR=Color(5,5,5,125)
DARK_COLOR=Color(0,0,4,0)

# LED strip configuration:
LED_COUNT = 144       # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.SK6812_STRIP_RGBW

MAX_TIME=LED_COUNT*60
print("Running for %i seconds (hours %.1f)"%(MAX_TIME,MAX_TIME/3600)) 

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

def fill(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)


def light_fill(left,nleds=LED_COUNT):
    lit = nleds-left/MAX_TIME * nleds
    return lit

def chase(left, leds, nmax=MAX_TIME):
    frac,base=modf(light_fill(left))
    for i in range(int(base)):
        leds.setPixelColor(i,DARK_COLOR)
    chaser=ceil(frac*base)
    leds.setPixelColor(chaser, SHINE_COLOR)
    leds.show()

def flash(leds):
    color=[255,128,0,0,0]
    random.shuffle(color)
    color=Color(*color[:4])
    halfled=int(LED_COUNT/2)
    for i in range(halfled):
        fill(leds,DARK_COLOR)
        leds.setPixelColor(halfled+i, color)
        leds.setPixelColor(halfled+i-1, color)
        leds.setPixelColor(halfled-i, color)
        leds.setPixelColor(halfled-i+1, color)
        time.sleep(0.01)
        leds.show()
    for i in range(random.randrange(1,5)):
        fill(leds,color)
        leds.show()
        time.sleep(.07)
        fill(leds,DARK_COLOR)
        leds.show()
        time.sleep(.4)

def effect(left, leds, nmax=MAX_TIME):
    if left > 0 and left < nmax :
        chase(left,leds)
    elif left <=0 and left > -120 :
        flash(leds)
    else:
        fill(leds, IDLE_COLOR)
        leds.show()

strip.begin()
today = datetime.date.today()
goal = datetime.datetime.combine(today,midnight).timestamp()
fill(strip,IDLE_COLOR)
strip.show()
while True:
    left = goal - time.time()
    effect(left,strip)

