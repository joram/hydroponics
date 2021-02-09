#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import atexit
import enum


class Pins(enum.Enum):
    PH_UP = 13
    PH_DOWN = 19
    NUTRIENTS = 26

GPIO.setmode(GPIO.BCM)
for pin in Pins:
    GPIO.setup(pin.value, GPIO.OUT)
    GPIO.output(pin.value, GPIO.LOW)


atexit.register(GPIO.cleanup)
for i in range(0,10):
    pin = 26
    
    GPIO.output(pin, GPIO.HIGH)
    print("high")
    time.sleep(2)

    GPIO.output(pin, GPIO.LOW)      
    print("low")
    time.sleep(2)
