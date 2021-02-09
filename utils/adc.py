#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from pipyadc.ADS1256_definitions import *
from pipyadc import ADS1256

if not os.path.exists("/dev/spidev0.1"):
    raise IOError("Error: No SPI device. Check settings in /boot/config.txt")

CHANNELS = {
    6: POS_AIN6,
    7: POS_AIN7,
}


def read_analog_values(channel_numbers):

    channels = []
    for channel in channel_numbers:
        if channel not in CHANNELS:
            raise Exception("channel does not exist")
        channels.append(CHANNELS[channel])

    ads = ADS1256()
    ads.cal_self()
    raw_channels = ads.read_sequence(channels)
    voltages = [i * ads.v_per_digit for i in raw_channels]
    return voltages

