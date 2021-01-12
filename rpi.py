from environs import Env
import atexit


env = Env()
if not env.bool("PRODUCTION", False):
    import sys
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)
