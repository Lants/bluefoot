import requests
import sys
from time import sleep

import brightness
import hw_api

def hw_run():

    BTN_UP = 40
    BTN_DWN = 38
    
    url = "http://127.0.0.1:5000/chungus"
    data_down = {'scroll-action': 'Down 0'}
    data_up = {'scroll-action': 'Up 0'}

    sensor = BrightnessSensor()
    adjust = BrightnessAdjuster()

    def scroll(channel):
        if (channel == BTN_UP):
            requests.post(url, data_up)
        elif (channel == BTN_DWN):
            requests.post(url, data_down)

    btn = Button()
    btn.setup_callback(scroll)

    while (1):
        adjust.brightness_adjustment(sensor)

hw_run()