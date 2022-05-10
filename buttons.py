#!/usr/bin/python3
import time
import RPi.GPIO as GPIO
import sys, signal
import argparse
import time

from pythonosc import udp_client

buttons = [18, 16, 38, 40] # GPIO PINS ON RPI

def button_pressed_callback(channel):
    for ind, val in enumerate(buttons):
        if channel == val:
            client.send_message("/channel", ind)
    #print(f"Button {channel} pressed!")

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

GPIO.setmode(GPIO.BOARD)
for buttonPin in buttons:
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=button_pressed_callback, bouncetime=250) 

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
