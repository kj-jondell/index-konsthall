#!/usr/bin/python3
import sys
import signal
import os
import time
#import argparse
import RPi.GPIO as GPIO

from pythonosc import udp_client

BUTTONS = [18, 16, 38, 40] # GPIO PINS ON RPI
SC_PORT = 57120 #use command line args instead?
try:
    SC_PORT = os.environ["SC_LISTEN_PORT"]
except KeyError:
    pass #Use default port if sc port not set

client = udp_client.SimpleUDPClient("127.0.0.1", SC_PORT)

def button_pressed_callback(channel):
    for ind, val in enumerate(BUTTONS):
        if channel == val:
            client.send_message("/channel", ind)
    #print(f"Button {channel} pressed!")

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

GPIO.setmode(GPIO.BOARD)
for buttonPin in BUTTONS:
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_pressed_callback, bouncetime=250) 

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
