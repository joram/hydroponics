#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from pipyadc.ADS1256_definitions import *
from pipyadc import ADS1256

if not os.path.exists("/dev/spidev0.1"):
    raise IOError("Error: No SPI device. Check settings in /boot/config.txt")

def read_analog_value(channel):
    channels = {
        6: POS_AIN6,
        7: POS_AIN7,
    }
    if channel not in channels:
        raise Exception("channel does not exist")
    ads = ADS1256()
    ads.cal_self()
    raw_channels = ads.read_sequence([channels[channel]])
    return raw_channels[0]

