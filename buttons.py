#!/usr/bin/python3
import sys
import signal
import os
import time
#import argparse
import RPi.GPIO as GPIO
from resettabletimer import ResettableTimer

from pythonosc import udp_client

BUTTONS = [18, 16, 38, 40] # GPIO PINS ON RPI
LEDS = [11, 13, 35, 37] # GPIO PINS ON RPI
TIME_OUT = 60*60 #seconds until reset
SC_PORT = 57120 #use command line args instead?
try:
    SC_PORT = os.environ["SC_LISTEN_PORT"]
except KeyError:
    pass #Use default port if sc port not set

channelStates = [1, 1, 1, 1] # states for the channel

client = udp_client.SimpleUDPClient("127.0.0.1", SC_PORT)

def reset_all():
    channelStates = [1, 1, 1, 1] # reset states
    for ledPin in LEDS: #reset leds
        GPIO.output(ledPin, GPIO.HIGH)
    client.send_message("/channel", channelStates) #reset channels
    timer.reset()

def button_pressed_callback(channel):
    for ind, val in enumerate(BUTTONS):
        if channel == val:
            channelStates[ind] = (channelStates[ind]+1)%2
            client.send_message("/channel", channelStates)
            GPIO.output(LEDS[ind], GPIO.HIGH if channelStates[ind] == 1 else GPIO.LOW)
            timer.reset()
    #print(f"Button {channel} pressed!")

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

GPIO.setmode(GPIO.BOARD)
for buttonPin in BUTTONS:
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_pressed_callback, bouncetime=250) 
for ledPin in LEDS:
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.HIGH)

timer = ResettableTimer(TIME_OUT, reset_all)
timer.start()

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
