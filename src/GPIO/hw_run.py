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
    BTN_TGL = 29    # Blue button
    
    # Information for post / get requests
    url = "http://127.0.0.1:5000/chungus"

    # Frames correspond to top left, right, and bottom left PDFs
    frames = [(1, 1), (1, 2), (2, 1)]
    cur = 0

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
            up_col_row = 'Up c' + frames[cur][0] + 'r' + frames[cur][1]
            data_up = {'scroll-action': up_col_row}
            requests.post(url, data_up)
        elif (channel == BTN_DWN):
            down_col_row = 'Down c' + frames[cur][0] + 'r' + frames[cur][1]
            data_down = {'scroll-action': down_col_row}
            requests.post(url, data_down)
        elif (channel == BTN_TGL):
            cur = (cur + 1) % 3

    # Set up buttons
    btn = hw_api.Button()
    btn.setup_callback(btn_func)

    # Launch brightness sensor
    adjust.brightness_adjustment(sensor)

hw_run()