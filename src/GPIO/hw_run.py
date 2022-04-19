import requests
import sys
from time import sleep

import brightness
import hw_api

# Run on launch for button and rotary encoder updates
def hw_run():

    BTN_UP = 40     # Green button
    BTN_DWN = 38    # Red button
    BTN_BRT = 22    # Yellow button
    
    # Information for post / get requests
    url = "http://127.0.0.1:5000/chungus"
    data_down = {'scroll-action': 'Down 0'}
    data_up = {'scroll-action': 'Up 0'}

    # Information for brightness sensor
    auto = True
    sensor = brightness.BrightnessSensor()
    adjust = brightness.BrightnessAdjuster()

    # Toggles between automatic and manual brightness adjustment
    # Scrolls PDF up and down
    def btn_func(channel):
        if (channel == BTN_BRT):
            if (adjust.AUTO == True):
                adjust.AUTO = False
            else:
                adjust.AUTO = True
        elif (channel == BTN_UP):
            requests.post(url, data_up)
        elif (channel == BTN_DWN):
            requests.post(url, data_down)

    # Set up buttons
    btn = hw_api.Button()
    btn.setup_callback(btn_func)

    # Launch brightness sensor
    adjust.brightness_adjustment(sensor)

hw_run()