import requests
import sys
from time import sleep

if __name__ == '__main__':
    url = "http://127.0.0.1:5000/chungus"
    data_down = {'scroll-action': 'Down 0'}
    data_up = {'scroll-action': 'Up 0'}

    if len(sys.argv) == 2 and sys.argv[1] == 'd':
        for i in range(0, 10):
            requests.post(url, data_down)

    if len(sys.argv) == 2 and sys.argv[1] == 'u':
        for i in range(0, 10):
            requests.post(url, data_up)